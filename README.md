# tools

Monorepo for small reusable Python tools.

Each tool is an installable package in its own subdirectory.

## Tool Catalog

1. `project_root_toolkit`
   - Resolve project root paths consistently across machines.
2. `repo_bootstrap_toolkit`
   - Generate baseline repo files for Commitizen + Python CI/CD.

## Install Any Tool From GitHub

Install directly from a subdirectory:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git#subdirectory=project_root_toolkit"
```

Use a tag for reproducible installs:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git@project_root_toolkit-v0.1.0#subdirectory=project_root_toolkit"
```

Replace `project_root_toolkit` with your target tool directory.


## Contributor Quick Start

Install all local tools in editable mode:

```bash
python devtools/install_tools.py --editable
```

Install one tool only:

```bash
python devtools/install_tools.py --editable --tool project_root_toolkit
```

Validate tool structure:

```bash
python devtools/check_tools.py
```

Validate one tool only:

```bash
python devtools/check_tools.py --tool project_root_toolkit
```

Run full local validation (same as CI logic):

```bash
python devtools/ci_validate_tools.py
```

Validate one tool only:

```bash
python devtools/ci_validate_tools.py --tool project_root_toolkit
```

## Devtools Folder

All CI/CD and contributor helper scripts are centralized in:

```text
devtools/
  check_tools.py
  ci_validate_tools.py
  detect_changed_tools.py
  install_tools.py
```

Local pre-PR flow:
1. `python devtools/check_tools.py`
2. `python devtools/ci_validate_tools.py`
3. Fix failures before opening a PR

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
1. `tool_name` uses lowercase with underscores.
2. Package uses `src/` layout.
3. `pyproject.toml` defines a unique `[project].name`.
4. Tool README includes install and usage examples.

## How To Build A New Tool

1. Create folder `tools/my_new_tool/`
2. Add required files:
   - `pyproject.toml`
   - `README.md`
   - `src/my_new_tool/__init__.py`
3. Optional: add CLI entry in `[project.scripts]`
4. Run checks:
   - `python devtools/check_tools.py --tool my_new_tool`
5. Build package locally:
   - `python -m pip install build`
   - `python -m build` (run inside tool directory)
6. Smoke test install:
   - `python -m pip install dist/<wheel-file>.whl`

## Version Control And Releases

Use semantic versioning in each tool's `pyproject.toml`.

Recommended tag format:
1. `<tool_name>-v<version>`
2. Example: `project_root_toolkit-v0.1.0`

Release flow:
1. Update version in `pyproject.toml`
2. Commit changes
3. Tag release
4. Push commit and tag
5. Consumers install using tagged Git URL

## CI/CD

Workflow:
1. `.github/workflows/tools-ci.yml`

Checks on PR and push to `main`:
1. Detect changed tool directories
2. `python devtools/check_tools.py --tool <changed_tool>`
3. `python devtools/ci_validate_tools.py --tool <changed_tool>`

If no tool package changed, CI exits early.

## Maintenance Checklist

Before committing:
1. No `__pycache__/`, `*.egg-info/`, `build/`, `dist/` checked in
2. `python devtools/check_tools.py` passes
3. Tool README matches current API
