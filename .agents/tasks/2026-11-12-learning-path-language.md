# Learning path language
Status: Complete — Language rules and existing paths updated; existing checker directory mismatch recorded below.

- [x] Add language guidance and update README and skills.
- [x] Translate Statistics, Omarchy, and the path index; preserve IDs, link targets, and checkbox progress (verified against HEAD).
- [x] Regenerate Statistics TOC with update_toc.py; run check_notes.py and git diff --check.

Corrected stale Learning/ references to the existing LearningPath/ directory in the affected documentation. Chinese aliases and original Anki card titles remain for lookup.

## Existing issue for follow-up

- [ ] Align scripts/check_notes.py with the existing LearningPath/ directory: its LEARNING constant is still "Learning". The checker reports no-parent for learning.org and unreachable for both paths. No files moved or node IDs changed in this task. TOC generation and whitespace checks passed.
