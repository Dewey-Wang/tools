# tools

Monorepo for small reusable Python tools.

Each subdirectory under `tools/` is an installable package.

## Install a tool

Install directly from GitHub subdirectory:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git#subdirectory=project_root_toolkit"
```

Use a version tag:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git@project_root_toolkit-v0.1.0#subdirectory=project_root_toolkit"
```

Replace `project_root_toolkit` with your target tool directory.

## Contributor Quick Start

Install all local tools in editable mode:

```bash
python install_tools.py --editable
```

Install one tool only:

```bash
python install_tools.py --editable --tool project_root_toolkit
```

Validate tool structure:

```bash
python check_tools.py
```

## Required Layout For Each Tool

```text
<tool_name>/
  pyproject.toml
  README.md
  src/
    <package_name>/
      __init__.py
```

Recommended:

```text
<tool_name>/
  tests/
  src/<package_name>/cli.py
  src/<package_name>/py.typed
```

Rules:
1. `tool_name` should use lowercase with underscores.
2. Package should use `src/` layout.
3. `pyproject.toml` must define a unique `[project].name`.
4. Tool README must include install and usage examples.

## How To Build A New Tool

1. Create a folder:
   - `tools/my_new_tool/`
2. Add required files:
   - `pyproject.toml`
   - `README.md`
   - `src/my_new_tool/__init__.py`
3. (Optional) Add CLI entry point in `pyproject.toml`:
   - `[project.scripts]`
4. Run checks:
   - `python check_tools.py`
5. Build package locally:
   - `python -m pip install build`
   - `python -m build` (run inside the tool directory)
6. Smoke test install:
   - `python -m pip install dist/<wheel-file>.whl`

## Version Control And Releases

Use semantic versioning in each tool's `pyproject.toml`:
- `0.1.0` for first usable release
- bump patch/minor/major as needed

Recommended tag format per tool:
- `<tool_name>-v<version>`
- example: `project_root_toolkit-v0.1.0`

Release flow:
1. Update version in `pyproject.toml`
2. Commit changes
3. Tag release
4. Push commit + tag
5. Consumers install using tag in Git URL

## Maintenance Checklist

Before committing:
1. No `__pycache__/`, `*.egg-info/`, `build/`, `dist/` checked in.
2. `python check_tools.py` passes.
3. Tool README matches current API.
