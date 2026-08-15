# Agent Workflow

## Core Principles
1. **Show a plan first**: state what you will read and edit before acting.
2. **Gather context first**: read the README, the target code, and
   `requirements.txt` before editing.
3. **Do not assume**: when in doubt, ask, or write it down as an explicit assumption.
4. **Minimal changes**: avoid refactors or edits beyond the requested scope.
5. **Verify after changes**: re-read edited files and, when possible,
   run/test the code.
6. **Report real logs**: always include actual output / tracebacks when
   reporting errors.

## Before Editing
- [ ] Read the README and the target files
- [ ] Confirmed existing naming and style conventions
- [ ] Understood the impact scope of the change

## After Editing
- [ ] Re-read the files and confirmed consistency
- [ ] Verified by running commands / tests
- [ ] Updated the README or these `.clinerules` if needed

## Before Committing
- Check the change set with `git status` / `git diff`.
- Make sure unintended files are excluded: `__pycache__/`, HTML exports
  (`*.html`), `data/result.jpg`, API keys.
