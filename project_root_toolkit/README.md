# project_root_toolkit

Portable project-root path resolution for local + HPC workflows.

## Install

From GitHub subdirectory:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git#subdirectory=project_root_toolkit"
```

From local `tools/` repo:

```bash
python -m pip install -e ./project_root_toolkit
```

## Core usage

```python
from pathlib import Path
from project_root_toolkit import resolve_project_root

CANDIDATES_DIR = (
    r"C:\Users\wani\Desktop\Work\HIV-Aanalysis",
    "/cfs/earth/scratch/wani/Desktop/HIV-Aanalysis",
)

PROJECT_ROOT = resolve_project_root(
    start=Path(__file__),
    candidates_dir=CANDIDATES_DIR,
    markers=(),  # candidates-only
)
```

Marker-only mode:

```python
PROJECT_ROOT = resolve_project_root(
    start=Path(__file__),
    candidates_dir=(),
    markers=(".git",),
)
```

## API

```python
resolve_project_root(
    start=None,
    *,
    candidates_dir=None,
    markers=(".git",),
    require_all_markers=False,
) -> Path
```

Resolution order:
1. First existing path in `candidates_dir`
2. Marker-based upward search (if `markers` is not empty)

## CLI

```bash
project-root-toolkit root --start ./notebooks --candidate-dir "C:\repo" --candidate-dir "/cfs/repo"
project-root-toolkit root --start ./notebooks --marker .git
project-root-toolkit init-config --output config.py --candidate-dir "C:\repo" --candidate-dir "/cfs/repo"
```

## Template

Starter template file:
- `src/project_root_toolkit/templates/config.py.tmpl`
