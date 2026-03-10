from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path

IGNORED_DIRS = {".git", "__pycache__"}


def discover_tools(root: Path) -> list[Path]:
    return sorted(
        [
            p
            for p in root.iterdir()
            if p.is_dir() and p.name not in IGNORED_DIRS and (p / "pyproject.toml").exists()
        ]
    )


def package_names(tool_dir: Path) -> list[str]:
    src_dir = tool_dir / "src"
    if not src_dir.is_dir():
        return []
    return sorted(
        [
            p.name
            for p in src_dir.iterdir()
            if p.is_dir() and p.name not in IGNORED_DIRS and not p.name.endswith(".egg-info")
        ]
    )


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd) if cwd else None)


def validate_tool(tool_dir: Path) -> None:
    names = package_names(tool_dir)
    if not names:
        raise RuntimeError(f"{tool_dir.name}: no package found under src/")

    # Install editable to validate metadata + dependencies.
    run([sys.executable, "-m", "pip", "install", "-e", str(tool_dir)])

    # Build wheel without pulling dependencies.
    dist_dir = tool_dir / ".ci-dist"
    if dist_dir.exists():
        for p in dist_dir.iterdir():
            if p.is_file():
                p.unlink()
    else:
        dist_dir.mkdir(parents=True)
    run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--wheel-dir",
            str(dist_dir),
            str(tool_dir),
        ]
    )

    # Import smoke test.
    code = "; ".join([f"import {name}" for name in names]) + "; print('import_ok')"
    run([sys.executable, "-c", code])
    shutil.rmtree(dist_dir, ignore_errors=True)


def main() -> None:
    root = Path(__file__).resolve().parent
    tools = discover_tools(root)
    if not tools:
        raise SystemExit("No tools found.")

    for tool in tools:
        print(f"\n=== Validating {tool.name} ===")
        validate_tool(tool)

    print("\nAll tools validated successfully.")


if __name__ == "__main__":
    main()
