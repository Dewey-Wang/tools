from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_FILES = ("pyproject.toml", "README.md")
REQUIRED_PACKAGE_FILE = "__init__.py"
IGNORED_DIRS = {".git", "__pycache__"}
DISALLOWED_DIR_NAMES = {"__pycache__"}
DISALLOWED_SUFFIXES = (".egg-info",)


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
        raise SystemExit("No tool packages found.")

    if not tool_names:
        return list(available.values())

    missing = [name for name in tool_names if name not in available]
    if missing:
        raise SystemExit(
            f"Unknown tool(s): {', '.join(missing)}. "
            f"Available: {', '.join(sorted(available))}"
        )
    return [available[name] for name in tool_names]


def check_tool(tool_dir: Path) -> list[str]:
    errors: list[str] = []

    for name in REQUIRED_FILES:
        if not (tool_dir / name).exists():
            errors.append(f"{tool_dir.name}: missing required file '{name}'")

    src_dir = tool_dir / "src"
    if not src_dir.is_dir():
        errors.append(f"{tool_dir.name}: missing 'src/' directory")
        return errors

    package_dirs = [
        p
        for p in src_dir.iterdir()
        if p.is_dir() and p.name not in IGNORED_DIRS and not p.name.endswith(".egg-info")
    ]
    if not package_dirs:
        errors.append(f"{tool_dir.name}: no package directory found under 'src/'")
        return errors

    if len(package_dirs) > 1:
        names = ", ".join(p.name for p in package_dirs)
        errors.append(f"{tool_dir.name}: multiple package dirs under src/: {names}")

    for pkg in package_dirs:
        if not (pkg / REQUIRED_PACKAGE_FILE).exists():
            errors.append(f"{tool_dir.name}: missing '{pkg.name}/{REQUIRED_PACKAGE_FILE}'")

    for p in tool_dir.rglob("*"):
        if not p.is_dir():
            continue
        if p.name in DISALLOWED_DIR_NAMES:
            errors.append(f"{tool_dir.name}: disallowed directory committed: '{p.relative_to(tool_dir)}'")
        if any(p.name.endswith(sfx) for sfx in DISALLOWED_SUFFIXES):
            errors.append(f"{tool_dir.name}: build artifact directory committed: '{p.relative_to(tool_dir)}'")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check tool package structure and repository hygiene."
    )
    parser.add_argument(
        "--tool",
        action="append",
        default=[],
        help="Tool folder name to check. Repeat for multiple tools.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    tools = select_tools(root, args.tool)

    all_errors: list[str] = []
    for tool in tools:
        all_errors.extend(check_tool(tool))

    if all_errors:
        print("Tool check failed:\n")
        for err in all_errors:
            print(f"- {err}")
        raise SystemExit(1)

    print(f"All checks passed ({len(tools)} tool(s)).")


if __name__ == "__main__":
    main()
