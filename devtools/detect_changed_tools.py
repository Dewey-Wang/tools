from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

IGNORED_DIRS = {".git", "__pycache__", "devtools", ".github"}


def discover_tools(root: Path) -> set[str]:
    return {
        p.name
        for p in root.iterdir()
        if p.is_dir() and p.name not in IGNORED_DIRS and (p / "pyproject.toml").exists()
    }


def changed_files(root: Path, base: str, head: str) -> list[str]:
    cmd = ["git", "diff", "--name-only", base, head]
    out = subprocess.check_output(cmd, cwd=str(root), text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def detect_changed_tools(root: Path, base: str, head: str) -> list[str]:
    tools = discover_tools(root)
    if base == "0000000000000000000000000000000000000000":
        return sorted(tools)
    files = changed_files(root, base, head)
    changed: set[str] = set()
    for rel in files:
        first = rel.split("/", 1)[0].split("\\", 1)[0]
        if first in tools:
            changed.add(first)
    return sorted(changed)


def write_github_outputs(path: Path, tools: list[str]) -> None:
    args = " ".join(f"--tool {name}" for name in tools)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"has_tools={'true' if tools else 'false'}\n")
        f.write(f"tools_json={json.dumps(tools)}\n")
        f.write(f"tools_args={args}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect changed tool directories between two git revisions."
    )
    parser.add_argument("--base", required=True, help="Base git revision")
    parser.add_argument("--head", required=True, help="Head git revision")
    parser.add_argument(
        "--github-output",
        default=None,
        help="Path to GITHUB_OUTPUT file for workflow outputs.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    tools = detect_changed_tools(root, args.base, args.head)
    print(json.dumps(tools))

    if args.github_output:
        write_github_outputs(Path(args.github_output), tools)


if __name__ == "__main__":
    main()
