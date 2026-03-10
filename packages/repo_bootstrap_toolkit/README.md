# repo_bootstrap_toolkit

Bootstrap helper for new or existing Python repositories.

It generates:
- `.cz.toml` (Commitizen configuration)
- `.github/workflows/python-ci.yml` (basic CI for Python + commit message check)

## Commitizen Reference

Official docs:

- https://commitizen-tools.github.io/commitizen/#what-commitizen-does

## Install

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git#subdirectory=packages/repo_bootstrap_toolkit"
```

## Quick Start

Run in a target repository:

```bash
repo-bootstrap-toolkit init --target .
```

Version behavior for generated `.cz.toml`:
- Toolkit always writes `version = "0.2.0"`.
- You can update it later with Commitizen bump commands.

Install Commitizen as a global CLI (recommended):

```bash
pipx install commitizen
pipx upgrade commitizen
```

Or with `uv`:

```bash
uv tool install commitizen
uv tool upgrade commitizen
```

Create commits with Conventional Commits prompts:

```bash
cz commit
```

Release/version bump from commit history:

```bash
cz bump
```

Common bump commands:

```bash
# Safe check before bumping
cz bump --check-consistency

# Auto-detect increment from commit history
cz bump

# Force increment type
cz bump --increment PATCH
cz bump --increment MINOR
cz bump --increment MAJOR
```

After bump:

```bash
git push origin main --follow-tags
```

## Daily Usage

1. Use `git add ...` to stage changes.
2. Run `cz commit` instead of `git commit`.
3. Push as usual.
4. When releasing, run `cz bump`, then push commit and tag.

## CLI

```text
repo-bootstrap-toolkit init [--target PATH] [--python-version 3.11] [--force]
```
