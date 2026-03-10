from __future__ import annotations

import argparse
from importlib import resources
from pathlib import Path

GENERATED_CZ_VERSION = "0.2.0"


def _read_template(name: str) -> str:
    return resources.files("repo_bootstrap_toolkit.templates").joinpath(name).read_text(
        encoding="utf-8"
    )


def _write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")


def init_repo(target: Path, python_version: str, force: bool) -> None:
    cz_template = _read_template("cz.toml.tmpl")
    cz_content = cz_template.format(version=GENERATED_CZ_VERSION)
    ci_template = _read_template("python_ci.yml.tmpl")
    ci_content = ci_template.format(python_version=python_version)

    _write_file(target / ".cz.toml", cz_content, force=force)
    _write_file(
        target / ".github" / "workflows" / "python-ci.yml",
        ci_content,
        force=force,
    )

    print("\nNext steps:")
    print(f"0) Generated .cz.toml with version = {GENERATED_CZ_VERSION}")
    print("1) Install Commitizen via pipx or uv:")
    print("   - pipx install commitizen")
    print("   - uv tool install commitizen")
    print("2) Use Commitizen:")
    print("   - cz commit")
    print("3) Bump version when releasing:")
    print("   - cz bump")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repo-bootstrap-toolkit",
        description="Scaffold Commitizen and CI files for a repository.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Generate .cz.toml and python-ci workflow")
    init_cmd.add_argument(
        "--target",
        default=".",
        help="Target repository directory.",
    )
    init_cmd.add_argument(
        "--python-version",
        default="3.11",
        help="Python version used in generated CI workflow.",
    )
    init_cmd.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        target = Path(args.target).expanduser().resolve()
        init_repo(target, python_version=args.python_version, force=args.force)


if __name__ == "__main__":
    main()
