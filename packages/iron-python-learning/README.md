# Iron Python Learning

This package is the Python learning track for Java engineers inside `iron-components-python`.

The goal is not to collect random notes. Each stage should have:

- a focused document that explains the idea through Java comparison;
- runnable Python code that can be debugged in PyCharm;
- a small bridge to later technical components and AI engineering work.

## Run

From the repository root:

```bash
uv run --package iron-python-learning python -m iron_python_learning
uv run --package iron-python-learning python -m iron_python_learning 3
```

The first command runs all stage demos. The second command runs a single stage.

## Current Shape

- `docs/stages/00-roadmap.md`: the 10-stage learning map.
- `docs/stages/python-language-stage-01-java-vs-python.md`: existing Stage 01 note, moved into the formal track.
- `docs/stages/python-language-stage-02-object-model-java-vs-python.md`: existing Stage 02 note, moved into the formal track.
- `docs/stages/python-language-stage-03-type-system-java-vs-python.md`: existing Stage 03 note, moved into the formal track.
- `docs/stages/stage-04-*.md` to `stage-10-*.md`: first-pass docs for the remaining stages.
- `src/iron_python_learning/stages/`: executable examples for each stage.

## Direction

This learning package can be adjusted later. For now it deliberately stays separate from real components like `iron-foundation`, `iron-message`, and `iron-cache`, so learning material will not pollute production component boundaries.
