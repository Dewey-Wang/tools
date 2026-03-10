# project_root_toolkit

A lightweight Python utility for **reliably resolving your project root directory** across different environments.

This is especially useful when the same code runs on:

* local machines
* HPC clusters
* remote servers
* CI pipelines

Instead of hard-coding paths or using fragile `../../..` hacks,
`project_root_toolkit` dynamically discovers your project root at runtime.

---

## Install

From GitHub subdirectory:

```bash
python -m pip install "git+https://github.com/Dewey-Wang/tools.git#subdirectory=packages/project_root_toolkit"
```

From local `tools/` repo:

```bash
python -m pip install -e ./packages/project_root_toolkit
```

---

# Quick start

Resolve the project root and build paths relative to it.

```python
from pathlib import Path
from project_root_toolkit import resolve_project_root

PROJECT_ROOT = resolve_project_root(start=Path(__file__))

data_path = PROJECT_ROOT / "data" / "dataset.csv"
```

Your code now works regardless of where it is executed.

---

## Core usage

## Multi-environment workflow (local + HPC)

You can provide multiple candidate directories.

The first existing path will be used.

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

## Marker-based detection

Alternatively, detect the project root by searching for marker files such as `.git`.

```python
PROJECT_ROOT = resolve_project_root(
    start=Path(__file__),
    candidates_dir=(),
    markers=(".git",),
)
```

The function walks upward from `start` until it finds a directory containing the marker.

---

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

---

## CLI

The toolkit also provides a command line interface.

Resolve the project root:


```bash
project-root-toolkit root --start ./notebooks --candidate-dir "C:\repo" --candidate-dir "/cfs/repo"
```

Marker-based resolution:

```bash
project-root-toolkit root --start ./notebooks --marker .git
```

Generate a starter configuration:

```bash
project-root-toolkit init-config --output config.py --candidate-dir "C:\repo" --candidate-dir "/cfs/repo"
```


---

## Template

Starter template file:
- `src/project_root_toolkit/templates/config.py.tmpl`


---

# License

MIT License
