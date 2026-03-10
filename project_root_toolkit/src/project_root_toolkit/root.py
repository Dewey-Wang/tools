from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Union

PathLike = Union[str, os.PathLike[str]]


def _resolve_candidate_path(candidate: PathLike, base_dir: Path) -> Path:
    path = Path(candidate).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def resolve_project_root(
    start: PathLike | None = None,
    *,
    candidates_dir: Iterable[PathLike] | None = None,
    markers: Iterable[str] = (".git",),
    require_all_markers: bool = False,
) -> Path:
    """Resolve a project root path.

    Resolution order:
    1. First existing path in ``candidates_dir``.
    2. Upward marker search from ``start`` (or current working directory).

    Parameters
    ----------
    start : str | os.PathLike | None, default None
        Starting location for relative candidate paths and fallback marker search.
        If a file path is provided, its parent directory is used.
        If ``None``, current working directory is used.
    candidates_dir : Iterable[str | os.PathLike] | None, default None
        Ordered candidate root paths. The first path that exists is returned.
        Relative paths are resolved against ``start``.
    markers : Iterable[str], default (".git",)
        Marker names for fallback upward search when no candidate path exists.
        Example markers: ``(".git",)`` or ``("pyproject.toml", ".git")``.
        Pass ``()`` to disable marker fallback.
    require_all_markers : bool, default False
        If ``False``, any marker match is accepted.
        If ``True``, all markers must exist in the same parent directory.

    Returns
    -------
    pathlib.Path
        Resolved project root path.

    Raises
    ------
    FileNotFoundError
        If no candidate exists and marker search does not find a match.

    Examples
    --------
    Candidates-only mode (recommended for local + HPC):

    >>> from pathlib import Path
    >>> resolve_project_root(
    ...     start=Path(__file__),
    ...     candidates_dir=(
    ...         r"C:\\Users\\wani\\Desktop\\Work\\HIV-Aanalysis",
    ...         "/cfs/earth/scratch/wani/Desktop/HIV-Aanalysis",
    ...     ),
    ...     markers=(),
    ... )

    Marker-only mode:

    >>> resolve_project_root(start=Path(__file__), candidates_dir=(), markers=(".git",))
    """
    probe = Path(start).expanduser().resolve() if start else Path.cwd().resolve()
    if probe.is_file():
        probe = probe.parent

    checked_candidates: list[Path] = []
    if candidates_dir:
        for candidate in candidates_dir:
            candidate_path = _resolve_candidate_path(candidate, probe)
            checked_candidates.append(candidate_path)
            if candidate_path.exists():
                return candidate_path

    marker_tuple = tuple(markers)
    if marker_tuple:
        for parent in (probe, *probe.parents):
            checks = tuple((parent / marker).exists() for marker in marker_tuple)
            if (all(checks) if require_all_markers else any(checks)):
                return parent

    details: list[str] = [f"Unable to resolve project root from {probe}."]
    if checked_candidates:
        details.append(
            "Candidate dirs checked: "
            + ", ".join(str(path) for path in checked_candidates)
        )
    else:
        details.append("No candidate dirs configured.")
    if marker_tuple:
        joined = ", ".join(marker_tuple)
        details.append(f"Markers checked: [{joined}]")
    else:
        details.append("No markers configured.")

    raise FileNotFoundError(
        " ".join(details)
    )


def project_path(
    *parts: str,
    start: PathLike | None = None,
    candidates_dir: Iterable[PathLike] | None = None,
    markers: Iterable[str] = (".git",),
    require_all_markers: bool = False,
) -> Path:
    """Build a path under the resolved project root.

    Parameters
    ----------
    *parts : str
        Path segments appended to the resolved project root.
    start, candidates_dir, markers, require_all_markers
        Same as :func:`resolve_project_root`.

    Returns
    -------
    pathlib.Path
        ``resolve_project_root(...) / Path(*parts)``
    """
    root = resolve_project_root(
        start=start,
        candidates_dir=candidates_dir,
        markers=markers,
        require_all_markers=require_all_markers,
    )
    return root.joinpath(*parts)
