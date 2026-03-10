from __future__ import annotations

from typing import Iterable


def _dirs_literal(candidates_dir: Iterable[str]) -> str:
    values = tuple(candidates_dir)
    if not values:
        return "()"
    return "(\n" + "".join(f"        {value!r},\n" for value in values) + "    )"


def render_config_template(
    *,
    candidates_dir: Iterable[str] = (),
    markers: Iterable[str] = (),
) -> str:
    marker_tuple = tuple(markers)
    marker_literal = ", ".join(repr(marker) for marker in marker_tuple)
    marker_expr = f"({marker_literal},)" if marker_tuple else "()"
    return (
        "from pathlib import Path\n"
        "from project_root_toolkit import resolve_project_root\n\n"
        "# Put your local/HPC root paths here (first existing path wins).\n"
        f"CANDIDATES_DIR = {_dirs_literal(candidates_dir)}\n\n"
        "# Resolve once, use everywhere.\n"
        "PROJECT_ROOT = resolve_project_root(\n"
        "    start=Path(__file__),\n"
        "    candidates_dir=CANDIDATES_DIR,\n"
        f"    markers={marker_expr},\n"
        ")\n\n"
        "DATA_DIR = PROJECT_ROOT / 'data'\n"
        "RESULTS_DIR = PROJECT_ROOT / 'results'\n"
    )
