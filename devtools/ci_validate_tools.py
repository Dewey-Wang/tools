from __future__ import annotations

import argparse
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


def select_tools(root: Path, tool_names: list[str]) -> list[Path]:
    available = {p.name: p for p in discover_tools(root)}
    if not available:
        raise SystemExit("No tools found.")

    if not tool_names:
        return list(available.values())

    missing = [name for name in tool_names if name not in available]
    if missing:
        raise SystemExit(
            f"Unknown tool(s): {', '.join(missing)}. "
            f"Available: {', '.join(sorted(available))}"
        )
    return [available[name] for name in tool_names]


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
    parser = argparse.ArgumentParser(
        description="Validate install/build/import for tool packages."
    )
    parser.add_argument(
        "--tool",
        action="append",
        default=[],
        help="Tool folder name to validate. Repeat for multiple tools.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    tools = select_tools(root, args.tool)

    for tool in tools:
        print(f"\n=== Validating {tool.name} ===")
        validate_tool(tool)

    print("\nAll tools validated successfully.")


if __name__ == "__main__":
    main()
