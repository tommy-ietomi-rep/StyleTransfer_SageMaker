# Git & Documentation Conventions

## Commit Messages
- Concise English in `type: summary` form (e.g., `add docker config`,
  `update code for latest`).
- One commit = one theme. Do not mix unrelated changes.
- Do not rewrite existing history (rebase, etc.).

## Branches
- Direct commits to `master` (main) are for small, one-off changes only.
- Create a feature branch for larger work.

## Documentation
- Keep README command examples and option tables in sync with the implementation.
- Update the README and the code together when behavior changes.

## Do Not Commit (Security)
- Never hardcode API keys or credentials in code.
- Never commit key files such as `DeepSeek_API.txt` (currently untracked —
  keep it that way).
- Do not commit changes to `StyleTransfer_SageMaker.html` (reference-only,
  although it is already tracked).
- Do not add secret files such as `.env`.
