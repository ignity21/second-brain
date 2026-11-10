"""Check org-roam notes against the structure and markup rules in AGENTS.md.

Usage:
    python3 scripts/check_notes.py [FILE.org ...]

With no arguments the whole library is checked.  With files, the whole
library is still parsed (the tree and links span files), but only problems
involving the given files are reported; files outside ``roamnotes-v2/``
(such as ``ankinotes/*.org``) get only the inline-markup check.

Checks:

- ``dangling-id``: an ``id:`` link to an ID that no note defines.
- ``missing-file``: a ``file:`` link to a path that does not exist.
- ``duplicate-id`` / ``duplicate-title``: two nodes share an ID, or a title or alias.
- ``multiple-parents``: a node is a main-tree child (``* [[id:...]]`` line) of more than one node.
- ``no-parent``: a note outside ``Unsorted/`` is neither a category root nor anyone's tree child.
- ``unreachable`` / ``too-deep``: a node cannot be reached from its category root,
  or sits below level 5.
- ``cross-category``: a tree child lives in a different category than its parent.
- ``out-degree``: a node has more than 8 tree children (more than 10 should get a new middle index).
- ``link-to-ancestor`` / ``link-to-index``: a body link points to the note's own tree ancestor,
  or to a pure navigation index.
- ``mutual-link``: two notes link each other in their bodies.
- ``link-to-learning``: a note outside ``Learning/`` links to a learning path.
- ``toc``: a note with more than 5 first- or second-level content headings has no TOC heading.
- ``markup``: inline markup glued to Chinese text, which Org does not render.

Exit status is 1 when anything is reported.
"""

import re
import sys
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIBRARY = REPO / "roamnotes-v2"
NON_CATEGORY_DIRS = {"assets"}
UNSORTED = "Unsorted"
LEARNING = "Learning"
MAX_LEVEL = 5
MAX_OUT_DEGREE = 8
MAX_HEADINGS_WITHOUT_TOC = 5

HEADING_RE = re.compile(r"^(\*+)\s+(.*?)\s*$")
ID_LINK_RE = re.compile(r"\[\[id:([^\]]+)\](?:\[[^\]]*\])?\]")
FILE_LINK_RE = re.compile(r"\[\[file:([^\]]+)\](?:\[[^\]]*\])?\]")
TREE_LINK_RE = re.compile(r"^\*+\s+\[\[id:([^\]]+)\]\[[^\]]*\]\]\s*(?::[\w@:]+:)?\s*$")
PROPERTY_RE = re.compile(r"^\s*:([A-Za-z_]+):\s*(.*?)\s*$")
TITLE_RE = re.compile(r"^#\+title:\s*(.*?)\s*$", re.I)
ALIAS_RE = re.compile(r'"([^"]+)"|(\S+)')
BLOCK_BEGIN_RE = re.compile(r"^\s*#\+begin_", re.I)
BLOCK_END_RE = re.compile(r"^\s*#\+end_", re.I)
TOC_TAG_RE = re.compile(r":toc(?:[@_]\d(?:[@_][a-z]+)?)?:", re.I)
CJK = r"[㐀-鿿豈-﫿，。；：！？、（）【】「」『』《》]"  # noqa: RUF001
# A closing marker after "+" is C++ or similar, not markup.
MARKUP_RE = re.compile(rf"{CJK}[*/_=+~](?=\S)|(?<=[^\s+])[*/_=+~]{CJK}")
# Link targets such as [[*标题]] or [[file:images/图/x.png]] are not markup.
LINK_TARGET_RE = re.compile(r"\[\[[^\]]*\]")


@dataclass(slots=True)
class Node:
    """An org-roam node: a file with an ID, or a heading with an ID."""

    id: str
    title: str
    path: Path
    line: int
    aliases: list[str] = field(default_factory=list)
    is_file: bool = True


@dataclass(frozen=True, slots=True)
class Link:
    """An ``id:`` link from the node enclosing it."""

    source: str
    target: str
    path: Path
    line: int
    is_tree: bool


@dataclass(frozen=True, slots=True)
class Problem:
    """One reported rule violation."""

    kind: str
    path: Path
    line: int
    message: str
    involves: frozenset[Path]

    def __str__(self) -> str:
        return f"{rel(self.path)}:{self.line}: {self.kind}: {self.message}"


@dataclass(slots=True)
class Library:
    """Everything parsed from the note files."""

    nodes: dict[str, Node] = field(default_factory=dict)
    links: list[Link] = field(default_factory=list)
    index_ids: set[str] = field(default_factory=set)
    problems: list[Problem] = field(default_factory=list)


def rel(path: Path) -> str:
    """Return PATH relative to the repository when possible."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def category(path: Path) -> str:
    """Return the category directory of a note file."""
    return path.relative_to(LIBRARY).parts[0]


def parse_aliases(value: str) -> list[str]:
    """Split a ``:ROAM_ALIASES:`` value into aliases."""
    return [quoted or bare for quoted, bare in ALIAS_RE.findall(value)]


def read_drawer(lines: list[str], start: int) -> tuple[dict[str, str], int]:
    """Read a property drawer opening at START; return its properties and the next line index."""
    props: dict[str, str] = {}
    if start >= len(lines) or lines[start].strip().upper() != ":PROPERTIES:":
        return props, start
    i = start + 1
    while i < len(lines) and lines[i].strip().upper() != ":END:":
        if m := PROPERTY_RE.match(lines[i]):
            props[m.group(1).upper()] = m.group(2)
        i += 1
    return props, i + 1


def outside_blocks(lines: list[str], start: int) -> Iterator[tuple[int, str]]:
    """Yield (index, line) from START on, skipping ``#+begin_``/``#+end_`` blocks."""
    in_block = False
    for i in range(start, len(lines)):
        line = lines[i]
        if in_block:
            in_block = not BLOCK_END_RE.match(line)
        elif BLOCK_BEGIN_RE.match(line):
            in_block = True
        else:
            yield i, line


@dataclass(slots=True)
class Headings:
    """Heading counts of one file, for the TOC and pure-index checks."""

    top: list[str] = field(default_factory=list)
    counts: dict[int, int] = field(default_factory=lambda: defaultdict(int))
    has_toc: bool = False

    def add(self, level: int, text: str, line: str) -> None:
        """Count one heading."""
        if TOC_TAG_RE.search(text):
            self.has_toc = True
        else:
            self.counts[level] += 1
        if level == 1:
            self.top.append(line)

    def is_index(self) -> bool:
        """Whether every first-level heading is a main-tree link."""
        return bool(self.top) and all(TREE_LINK_RE.match(h) for h in self.top)


def parse_file(path: Path, lib: Library) -> None:
    """Parse one note file into nodes, links and problems."""
    lines = path.read_text(encoding="utf-8").splitlines()
    props, body_start = read_drawer(lines, 0)
    title = next((m.group(1) for ln in lines if (m := TITLE_RE.match(ln))), path.stem)
    file_id = props.get("ID")
    if file_id:
        add_node(lib, Node(file_id, title, path, 1, parse_aliases(props.get("ROAM_ALIASES", ""))))
    # Stack of (heading level, node ID) for headings that carry an ID.
    stack: list[tuple[int, str]] = []
    headings = Headings()
    for i, line in outside_blocks(lines, body_start):
        if m := HEADING_RE.match(line):
            headings.add(len(m.group(1)), m.group(2), line)
            enter_heading(lib, path, lines, i, m, stack)
        # A tree line under an ID heading still makes the file the parent; body
        # links belong to the innermost node.
        source = file_id if TREE_LINK_RE.match(line) or not stack else stack[-1][1]
        collect_links(lib, path, i + 1, line, source)
    if not file_id:
        return
    if headings.is_index():
        lib.index_ids.add(file_id)
    elif not headings.has_toc:
        check_toc(lib, path, headings.counts)


def enter_heading(
    lib: Library,
    path: Path,
    lines: list[str],
    i: int,
    m: re.Match[str],
    stack: list[tuple[int, str]],
) -> None:
    """Update the stack of enclosing ID headings for the heading M on line I."""
    level, text = len(m.group(1)), m.group(2)
    while stack and stack[-1][0] >= level:
        stack.pop()
    heading_props, _ = read_drawer(lines, i + 1)
    if heading_id := heading_props.get("ID"):
        aliases = parse_aliases(heading_props.get("ROAM_ALIASES", ""))
        add_node(lib, Node(heading_id, text, path, i + 1, aliases, is_file=False))
        stack.append((level, heading_id))


def add_node(lib: Library, node: Node) -> None:
    """Register NODE, reporting a duplicate ID."""
    if other := lib.nodes.get(node.id):
        lib.problems.append(
            Problem(
                "duplicate-id",
                node.path,
                node.line,
                f"{node.id} also defined in {rel(other.path)}:{other.line}",
                frozenset({node.path, other.path}),
            )
        )
        return
    lib.nodes[node.id] = node


def collect_links(lib: Library, path: Path, lineno: int, line: str, source: str | None) -> None:
    """Record the ``id:`` links on LINE and check its ``file:`` links."""
    tree = TREE_LINK_RE.match(line)
    for m in ID_LINK_RE.finditer(line):
        if source:
            lib.links.append(Link(source, m.group(1), path, lineno, is_tree=bool(tree)))
    for m in FILE_LINK_RE.finditer(line):
        target = m.group(1).split("::", 1)[0]
        resolved = Path(target).expanduser()
        if not resolved.is_absolute():
            resolved = path.parent / resolved
        if not resolved.exists():
            lib.problems.append(Problem("missing-file", path, lineno, target, frozenset({path})))


def check_toc(lib: Library, path: Path, level_counts: dict[int, int]) -> None:
    """Report a note that has enough headings to need a TOC but has none."""
    first, second = level_counts.get(1, 0), level_counts.get(2, 0)
    if first > MAX_HEADINGS_WITHOUT_TOC or second > MAX_HEADINGS_WITHOUT_TOC:
        tag = ":TOC_2:" if second > MAX_HEADINGS_WITHOUT_TOC else ":TOC_1:"
        message = f"{first} first-level and {second} second-level headings; add * TOC {tag}"
        lib.problems.append(Problem("toc", path, 1, message, frozenset({path})))


def check_ids_and_titles(lib: Library) -> None:
    """Report dangling ID links and titles or aliases shared by several nodes."""
    for link in lib.links:
        if link.target not in lib.nodes:
            lib.problems.append(
                Problem("dangling-id", link.path, link.line, link.target, frozenset({link.path}))
            )
    by_name: dict[str, list[Node]] = defaultdict(list)
    for node in lib.nodes.values():
        for name in {node.title, *node.aliases}:
            by_name[name.casefold()].append(node)
    for name, nodes in by_name.items():
        if len(nodes) > 1:
            first = nodes[0]
            others = ", ".join(f"{rel(n.path)}:{n.line}" for n in nodes[1:])
            lib.problems.append(
                Problem(
                    "duplicate-title",
                    first.path,
                    first.line,
                    f"{name!r} also used by {others}",
                    frozenset(n.path for n in nodes),
                )
            )


def tree_edges(lib: Library) -> dict[str, list[str]]:
    """Return each node's parents along the main tree."""
    parents: dict[str, list[str]] = defaultdict(list)
    for link in lib.links:
        if link.is_tree and link.target in lib.nodes:
            parents[link.target].append(link.source)
    return parents


def is_root(node: Node) -> bool:
    """Whether NODE is its category's root index, named after the directory.

    The file stem or title matches the directory, ignoring case, spaces and
    underscores, with ``+`` read as ``p``: ``LinearAlgebra/linear_algebra.org``,
    ``Elisp/elisp.org`` and ``C++/cpp.org``.
    """
    if not node.is_file:
        return False
    cat = normalize_name(category(node.path))
    return cat in (normalize_name(node.path.stem), normalize_name(node.title))


def normalize_name(name: str) -> str:
    """Lowercase NAME, read ``+`` as ``p`` and drop everything but letters and digits."""
    return re.sub(r"[^a-z0-9]", "", name.casefold().replace("+", "p"))


def problem_for(kind: str, node: Node, message: str, *others: Node) -> Problem:
    """Build a problem located at NODE that also involves OTHERS."""
    return Problem(
        kind, node.path, node.line, message, frozenset({node.path, *(o.path for o in others)})
    )


def check_tree(lib: Library, parents: dict[str, list[str]]) -> dict[str, int]:
    """Check parents, reachability, depth and out-degree; return each reachable node's level."""
    children: dict[str, list[str]] = defaultdict(list)
    for child, ps in parents.items():
        for p in ps:
            children[p].append(child)
    levels = tree_levels(lib, children)
    for node in lib.nodes.values():
        check_node_place(lib, node, parents.get(node.id, []), levels)
    for node_id, kids in children.items():
        if len(kids) > MAX_OUT_DEGREE:
            node = lib.nodes[node_id]
            lib.problems.append(problem_for("out-degree", node, f"{len(kids)} tree children"))
    return levels


def tree_levels(lib: Library, children: dict[str, list[str]]) -> dict[str, int]:
    """Return the level of every node reachable from a category root (roots are level 1)."""
    frontier = [n.id for n in lib.nodes.values() if is_root(n)]
    levels = dict.fromkeys(frontier, 1)
    level = 1
    while frontier:
        level += 1
        nxt = [c for node_id in frontier for c in children.get(node_id, []) if c not in levels]
        frontier = list(dict.fromkeys(nxt))
        levels.update(dict.fromkeys(frontier, level))
    return levels


def check_parents(lib: Library, node: Node, parents: list[str]) -> None:
    """Report a node with several tree parents, or a parent in another category."""
    unique = sorted(set(parents))
    if len(unique) > 1:
        names = ", ".join(lib.nodes[p].title for p in unique)
        lib.problems.append(
            problem_for("multiple-parents", node, names, *(lib.nodes[p] for p in unique))
        )
    for parent in (lib.nodes[p] for p in unique):
        if category(parent.path) != category(node.path):
            message = f"tree child of {parent.title} in {category(parent.path)}/"
            lib.problems.append(problem_for("cross-category", node, message, parent))


def check_node_place(lib: Library, node: Node, parents: list[str], levels: dict[str, int]) -> None:
    """Check one node's parents, category, reachability and depth."""
    check_parents(lib, node, parents)
    if category(node.path) == UNSORTED or is_root(node):
        return
    if not parents and node.is_file:
        lib.problems.append(problem_for("no-parent", node, "not linked from any index"))
    elif not parents:
        return
    elif node.id not in levels:
        lib.problems.append(problem_for("unreachable", node, "not reachable from a category root"))
    elif levels[node.id] > MAX_LEVEL:
        lib.problems.append(problem_for("too-deep", node, f"level {levels[node.id]}"))


def ancestors(node_id: str, parents: dict[str, list[str]]) -> set[str]:
    """Return every tree ancestor of NODE_ID."""
    seen: set[str] = set()
    todo = list(parents.get(node_id, []))
    while todo:
        p = todo.pop()
        if p not in seen:
            seen.add(p)
            todo.extend(parents.get(p, []))
    return seen


def file_node_of(lib: Library, node_id: str) -> str:
    """Return the file node containing NODE_ID (itself for a file node)."""
    node = lib.nodes[node_id]
    if node.is_file:
        return node_id
    return next((n.id for n in lib.nodes.values() if n.is_file and n.path == node.path), node_id)


def check_body_link(
    lib: Library, link: Link, parents: dict[str, list[str]]
) -> tuple[str, str] | None:
    """Check one body link; return its (source file, target file) pair if it crosses files."""
    if link.is_tree or link.target not in lib.nodes or link.source not in lib.nodes:
        return None
    source, target = lib.nodes[link.source], lib.nodes[link.target]
    src_file, dst_file = file_node_of(lib, source.id), file_node_of(lib, target.id)
    if src_file == dst_file:
        return None
    involved = frozenset({link.path, target.path})
    kinds = []
    if category(target.path) == LEARNING and category(source.path) != LEARNING:
        kinds.append("link-to-learning")
    if target.id in ancestors(source.id, parents) | ancestors(src_file, parents):
        kinds.append("link-to-ancestor")
    elif target.id in lib.index_ids:
        kinds.append("link-to-index")
    for kind in kinds:
        lib.problems.append(Problem(kind, link.path, link.line, target.title, involved))
    return src_file, dst_file


def check_body_links(lib: Library, parents: dict[str, list[str]]) -> None:
    """Check body links for ancestors, indexes, learning paths and mutual pairs."""
    pairs: dict[tuple[str, str], Link] = {}
    for link in lib.links:
        if pair := check_body_link(lib, link, parents):
            pairs.setdefault(pair, link)
    for (a, b), link in pairs.items():
        if a >= b or (b, a) not in pairs:
            continue
        back = pairs[(b, a)]
        names = f"{lib.nodes[a].title} <-> {lib.nodes[b].title}"
        message = f"{names} (also {rel(back.path)}:{back.line})"
        involved = frozenset({link.path, back.path})
        lib.problems.append(Problem("mutual-link", link.path, link.line, message, involved))


def check_markup(path: Path) -> list[Problem]:
    """Report inline markup glued to Chinese text in PATH."""
    problems = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if m := MARKUP_RE.search(LINK_TARGET_RE.sub(lambda t: " " * len(t.group()), line)):
            snippet = line[max(0, m.start() - 8) : m.end() + 8].strip()
            problems.append(Problem("markup", path, lineno, snippet, frozenset({path})))
    return problems


def note_files() -> list[Path]:
    """Return every note file in the library."""
    return sorted(
        p
        for p in LIBRARY.rglob("*.org")
        if p.relative_to(LIBRARY).parts[0] not in NON_CATEGORY_DIRS
        and not any(part.startswith(".") for part in p.relative_to(LIBRARY).parts)
    )


def check_library() -> Library:
    """Parse and check the whole library."""
    lib = Library()
    for path in note_files():
        parse_file(path, lib)
        lib.problems.extend(check_markup(path))
    check_ids_and_titles(lib)
    parents = tree_edges(lib)
    check_tree(lib, parents)
    check_body_links(lib, parents)
    return lib


def select_problems(lib: Library, targets: set[Path]) -> list[Problem]:
    """Keep the problems involving TARGETS, or all when there are none.

    Targets outside the library, such as Anki files, get only the markup check.
    """
    if not targets:
        return lib.problems
    problems = [p for p in lib.problems if p.involves & targets]
    for path in sorted(t for t in targets if not t.is_relative_to(LIBRARY)):
        problems.extend(check_markup(path))
    return problems


def main(argv: list[str]) -> int:
    """Run the checks and print problems; return the exit status."""
    targets = {Path(a).resolve() for a in argv}
    for missing in sorted(t for t in targets if not t.exists()):
        print(f"{missing}: no such file", file=sys.stderr)
        return 2
    problems = select_problems(check_library(), targets)
    for problem in sorted(set(problems), key=lambda p: (rel(p.path), p.line, p.kind)):
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
