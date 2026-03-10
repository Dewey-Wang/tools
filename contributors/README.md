# Contributor Guide

This folder contains contributor docs and helper scripts for the `tools` monorepo.

## Folder Layout

```text
packages/
  <tool_name>/
    pyproject.toml
    README.md
    src/
      <package_name>/
        __init__.py
contributors/
  README.md
  devtools/
    check_tools.py
    ci_validate_tools.py
    detect_changed_tools.py
    install_tools.py
```

## Rules For New Tools

1. Tool folder name must be lowercase with underscores.
2. Each tool must use `src/` layout.
3. Each tool must have a unique `[project].name` in `pyproject.toml`.
4. Each tool must include install and usage examples in its own `README.md`.

Required structure:

```text
packages/<tool_name>/
  pyproject.toml
  README.md
  src/
    <package_name>/
      __init__.py
```

Recommended additions:

```text
packages/<tool_name>/
  tests/
  src/<package_name>/cli.py
  src/<package_name>/py.typed
```

## Local Development Workflow

Install all tools in editable mode:

```bash
python contributors/devtools/install_tools.py --editable
```

Install only one tool:

```bash
python contributors/devtools/install_tools.py --editable --tool project_root_toolkit
```

Run structure checks:

```bash
python contributors/devtools/check_tools.py
```

Run checks for one tool:

```bash
python contributors/devtools/check_tools.py --tool project_root_toolkit
```

Run full validation (install/build/import):

```bash
python contributors/devtools/ci_validate_tools.py
```

Run full validation for one tool:

```bash
python contributors/devtools/ci_validate_tools.py --tool project_root_toolkit
```

## CI Notes

Main workflow: `.github/workflows/tools-ci.yml`

CI behavior:
1. Detect changed tool directories.
2. Validate structure for changed tools.
3. Validate install/build/import for changed tools.
4. Exit early when no tool package changed.

## Versioning And Release

1. Use semantic versioning in each tool `pyproject.toml`.
2. Recommended tag format: `<tool_name>-v<version>`.
3. Example: `project_root_toolkit-v0.1.0`.

Release flow:
1. Update version in `pyproject.toml`.
2. Commit changes.
3. Create tag.
4. Push commit and tag.


## Maintenance Checklist

Before committing:
1. No `__pycache__/`, `*.egg-info/`, `build/`, `dist/` checked in
2. `python contributors/devtools/check_tools.py` passes
3. Tool README matches current API
