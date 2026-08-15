# Coding Standards

## General
- **Follow the style of the existing code above all else.**
- Comments may be written in Japanese (matching existing code); identifiers,
  API names, logs, and commit messages are in English.
- Do not create unnecessary files. If you add a file, document its purpose
  (e.g., in the README).

## Python (`scripts/`, etc.)
- Follow PEP 8 (line length ~100 chars max).
- CLI must use `argparse` with long options (`--xxx`).
- Add a module-level docstring including a Usage example.
- Constants are UPPER_SNAKE_CASE (e.g., `STYLE_WEIGHTS`, `CONTENT_WEIGHT`).
- Section divider comments use the existing `# --- ...` style.
- When adding a dependency, update `requirements.txt` in the same change.

## Verilog (`verilog/` learning samples)
- Add a header comment at the top of each module (purpose, reference docs, caveats).
- Use `//===...` section divider style.
- Japanese comments are fine; cite reference documents (e.g., UG472) with page numbers.

## Notebooks
- Keep cells in an order that is easy to follow.
- Do not commit new HTML exports (`*.html`).
