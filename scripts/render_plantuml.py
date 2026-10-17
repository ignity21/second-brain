"""Render the PlantUML src blocks of org notes, as org-babel would.

Usage: python3 scripts/render_plantuml.py NOTE.org...

Each ``#+begin_src plantuml :file PATH`` block is rendered with the local
``plantuml`` executable to PATH, relative to the note.  An image is rewritten
only when its content changes (PlantUML output is deterministic).  A block
not yet followed by ``#+RESULTS:`` gets one linking to PATH, so the note reads
the same as after ``C-c C-c`` in Emacs.  Blocks without ``:file`` are skipped.
"""

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

BEGIN_RE = re.compile(r"^(?P<indent>[ \t]*)#\+begin_src[ \t]+plantuml\b(?P<args>.*)$", re.I)
END_RE = re.compile(r"^[ \t]*#\+end_src[ \t]*$", re.I)
RESULTS_RE = re.compile(r"^[ \t]*#\+results(\[.*\])?:", re.I)
FILE_ARG_RE = re.compile(r":file[ \t]+(\S+)")
# Org escapes lines starting with `*' or `#+' inside blocks with a comma.
ESCAPE_RE = re.compile(r"^([ \t]*),(?=\*|#\+)", re.M)


class RenderError(Exception):
    """PlantUML failed to render a block."""


@dataclass(frozen=True, slots=True)
class Block:
    """A PlantUML src block with a ``:file`` target.

    :param begin: index of the ``#+begin_src`` line.
    :param end: index of the ``#+end_src`` line.
    :param indent: indentation of the ``#+begin_src`` line.
    :param target: the ``:file`` path as written.
    :param source: the block body, unescaped.
    """

    begin: int
    end: int
    indent: str
    target: str
    source: str


def find_blocks(lines: list[str]) -> list[Block]:
    """Return the PlantUML blocks with a ``:file`` argument in LINES."""
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        begin = BEGIN_RE.match(lines[i])
        if not begin:
            i += 1
            continue
        end = next((j for j in range(i + 1, len(lines)) if END_RE.match(lines[j])), None)
        if end is None:
            break
        target = FILE_ARG_RE.search(begin["args"])
        if target:
            source = ESCAPE_RE.sub(r"\1", "".join(lines[i + 1 : end]))
            blocks.append(Block(i, end, begin["indent"], target[1], source))
        i = end + 1
    return blocks


def render(source: str, image: Path) -> bool:
    """Render SOURCE to IMAGE, in the format its extension names.

    :returns: whether IMAGE was written.
    :raises RenderError: if PlantUML reports an error.
    """
    result = subprocess.run(
        ["plantuml", f"-t{image.suffix.lstrip('.')}", "-pipe"],
        input=source.encode(),
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        # PlantUML reports `ERROR', the line number and the message on separate lines.
        message = " ".join(result.stderr.decode().split())
        raise RenderError(f"{image}: {message}")
    if image.exists() and image.read_bytes() == result.stdout:
        return False
    image.parent.mkdir(parents=True, exist_ok=True)
    _ = image.write_bytes(result.stdout)
    return True


def has_results(lines: list[str], end: int) -> bool:
    """Whether the block ending at line END is followed by ``#+RESULTS:``."""
    following = (line for line in lines[end + 1 :] if line.strip())
    return bool(RESULTS_RE.match(next(following, "")))


def process(note: Path) -> list[str]:
    """Render NOTE's blocks and add missing results.

    :returns: a description of each change made.
    :raises RenderError: if any block fails to render.
    """
    lines = note.read_text().splitlines(keepends=True)
    changes: list[str] = []
    # Bottom-up, so inserting results keeps earlier line indices valid.
    for block in reversed(find_blocks(lines)):
        block_changes: list[str] = []
        if render(block.source, note.parent / block.target):
            block_changes.append(f"rendered {block.target}")
        if not has_results(lines, block.end):
            results = f"\n{block.indent}#+RESULTS:\n{block.indent}[[file:{block.target}]]\n"
            following = lines[block.end + 1 : block.end + 2]
            if following and following[0].strip():
                results += "\n"
            lines.insert(block.end + 1, results)
            block_changes.append(f"linked {block.target}")
        changes[:0] = block_changes
    if any(c.startswith("linked") for c in changes):
        _ = note.write_text("".join(lines))
    return changes


def main(argv: list[str]) -> int:
    """Process each note named in ARGV; return the exit status."""
    if not argv:
        print("Usage: python3 scripts/render_plantuml.py NOTE.org...", file=sys.stderr)
        return 2
    status = 0
    for name in argv:
        try:
            for change in process(Path(name)):
                print(f"{name}: {change}")
        except RenderError as e:
            print(f"{name}: error: {e}", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
