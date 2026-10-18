"""Regenerate the toc-org tables of contents of org notes, as saving in Emacs would.

Usage: python3 scripts/update_toc.py NOTE.org...

In the user's Doom Emacs, ``toc-org-mode`` rewrites the ``:TOC:`` heading's
entries on save.  This runs the same ``toc-org-insert-toc`` in a batch Emacs
that loads only org and toc-org from Doom's straight build, so no running
Emacs is needed and the output matches a save in Emacs.  A note is written
only when its TOC changes; notes without a TOC heading are left alone.

toc-org replaces everything between the TOC heading and the next heading, so
a note with other text there is reported and skipped rather than losing it.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

PACKAGES = ("org", "toc-org")
HEADING_RE = re.compile(r"^\*+\s")
# The heading tags toc-org looks for: :TOC:, :TOC_2:, :TOC_2_gh: and the like.
TOC_HEADING_RE = re.compile(r"^\*+\s.*:toc(?:[@_]\d(?:[@_][a-z]+)?)?:", re.I)
# What toc-org writes under the heading: list entries, wrapped in a quote for :QUOTE:.
TOC_LINE_RE = re.compile(r"^\s*(?:- \[\[#.*\]\]|#\+(?:begin|end)_quote)\s*$", re.I)
# Prints each file whose TOC changed; backups and lock files would litter the repo.
ELISP = """
(progn
  (setq make-backup-files nil create-lockfiles nil)
  (require 'org)
  (require 'toc-org)
  (dolist (file command-line-args-left)
    (with-current-buffer (find-file-noselect file)
      (toc-org-insert-toc)
      (when (buffer-modified-p)
        (save-buffer)
        (princ (format "%s\\n" file)))))
  (setq command-line-args-left nil))
"""


class SetupError(Exception):
    """Emacs or the packages toc-org needs are missing."""


def emacs_version() -> str:
    """Return the version of the ``emacs`` on PATH, as straight names build dirs."""
    try:
        result = subprocess.run(
            ["emacs", "--batch", "-Q", "--eval", "(princ emacs-version)"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as e:
        raise SetupError(f"cannot run emacs: {e}") from e
    return result.stdout.strip()


def package_dirs() -> list[Path]:
    """Return the straight build dirs of org and toc-org for the current Emacs.

    :raises SetupError: if Emacs or a package is missing.
    """
    emacs_dir = Path(os.environ.get("EMACSDIR", "~/.config/emacs")).expanduser()
    build = emacs_dir / ".local" / "straight" / f"build-{emacs_version()}"
    dirs = [build / name for name in PACKAGES]
    missing = [str(d) for d in dirs if not d.is_dir()]
    if missing:
        raise SetupError(f"missing package dirs (run `doom sync`?): {', '.join(missing)}")
    return dirs


def stray_lines(text: str) -> list[str]:
    """Return the lines under TEXT's TOC heading that toc-org would discard."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if TOC_HEADING_RE.match(line)), None)
    if start is None:
        return []
    stray: list[str] = []
    for line in lines[start + 1 :]:
        if HEADING_RE.match(line):
            break
        if line.strip() and not TOC_LINE_RE.match(line):
            stray.append(line)
    return stray


def update(notes: list[str]) -> list[str]:
    """Regenerate the TOCs of NOTES.

    :returns: the notes whose TOC changed.
    :raises SetupError: if Emacs or a package is missing, or Emacs fails.
    """
    load_path = [arg for d in package_dirs() for arg in ("-L", str(d))]
    result = subprocess.run(
        ["emacs", "--batch", "-Q", *load_path, "--eval", ELISP, *notes],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SetupError(f"emacs failed: {result.stderr.strip()}")
    return result.stdout.splitlines()


def main(argv: list[str]) -> int:
    """Update each note named in ARGV; return the exit status."""
    if not argv:
        print("Usage: python3 scripts/update_toc.py NOTE.org...", file=sys.stderr)
        return 2
    missing = [name for name in argv if not Path(name).is_file()]
    if missing:
        print(f"error: no such file: {', '.join(missing)}", file=sys.stderr)
        return 2
    status = 0
    safe: list[str] = []
    for name in argv:
        stray = stray_lines(Path(name).read_text())
        if stray:
            print(f"{name}: error: text under the TOC heading: {stray[0]}", file=sys.stderr)
            status = 1
        else:
            safe.append(name)
    if not safe:
        return status
    try:
        for name in update(safe):
            print(f"{name}: updated TOC")
    except SetupError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
