from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PACKAGES_DIR_NAME = "packages"


def discover_tool_dirs(root: Path) -> list[Path]:
    packages_dir = root / PACKAGES_DIR_NAME
    if not packages_dir.is_dir():
        return []
    return sorted(
        [
            d
            for d in packages_dir.iterdir()
            if d.is_dir() and (d / "pyproject.toml").exists()
        ]
    )


def install_tool(path: Path, editable: bool) -> None:
    cmd = [sys.executable, "-m", "pip", "install"]
    if editable:
        cmd.append("-e")
    cmd.append(str(path))
    print(f"Installing: {path.name}")
    subprocess.check_call(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install tool packages from this tools monorepo."
    )
    parser.add_argument(
        "--tool",
        action="append",
        default=[],
        help="Tool folder name to install. Repeat for multiple tools.",
    )
    parser.add_argument(
        "--editable",
        action="store_true",
        help="Install in editable mode.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    available = {d.name: d for d in discover_tool_dirs(root)}
    if not available:
        raise SystemExit("No tool packages found (missing pyproject.toml).")

    selected = args.tool or list(available.keys())
    missing = [name for name in selected if name not in available]
    if missing:
        raise SystemExit(
            f"Unknown tool(s): {', '.join(missing)}. "
            f"Available: {', '.join(sorted(available))}"
        )

    for name in selected:
        install_tool(available[name], editable=args.editable)

    print("Done.")


if __name__ == "__main__":
    main()
