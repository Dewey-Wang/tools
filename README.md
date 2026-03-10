# tools

Monorepo for small reusable Python tools.

Tool packages are located under `packages/` and can be installed directly from GitHub.

## Available Tools

`project_root_toolkit`
- Resolve project root paths consistently across local machines and HPC.

`repo_bootstrap_toolkit`
- Generate starter files for Commitizen and a Python CI workflow.

## Quick Install

Install one tool from GitHub:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git#subdirectory=packages/project_root_toolkit"
```

Install from a release tag:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git@project_root_toolkit-v0.1.0#subdirectory=packages/project_root_toolkit"
```

Replace `project_root_toolkit` with the tool folder you want.

## Quick Use Example

See the README.md in the tool to have a quick start.

## For Contributors

Contributor rules, structure requirements, local validation, and release steps are documented here:

`contributors/README.md`
