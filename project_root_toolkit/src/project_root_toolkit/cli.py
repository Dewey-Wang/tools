from __future__ import annotations

import argparse
from pathlib import Path

from .root import resolve_project_root
from .template import render_config_template


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project-root-toolkit",
        description="Project-root utilities for analysis repos.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    root_cmd = sub.add_parser("root", help="Print resolved project root")
    root_cmd.add_argument(
        "--start",
        default=None,
        help="Starting path for upward search (file or directory).",
    )
    root_cmd.add_argument(
        "--candidate-dir",
        action="append",
        default=[],
        help="Candidate root directory path. Repeat for multiple candidates.",
    )
    root_cmd.add_argument(
        "--marker",
        action="append",
        default=[],
        help="Marker to search for. Repeat for multiple markers.",
    )
    root_cmd.add_argument(
        "--require-all-markers",
        action="store_true",
        help="Require all markers to exist in the same parent directory.",
    )

    init_cmd = sub.add_parser("init-config", help="Write a starter config.py")
    init_cmd.add_argument(
        "--output",
        default="config.py",
        help="Output path for generated config file.",
    )
    init_cmd.add_argument(
        "--candidate-dir",
        action="append",
        default=[],
        help="Candidate root directory path. Repeat for multiple candidates.",
    )
    init_cmd.add_argument(
        "--marker",
        action="append",
        default=[],
        help="Marker to search for. Repeat for multiple markers.",
    )
    init_cmd.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "root":
        markers = tuple(args.marker)
        root = resolve_project_root(
            start=args.start,
            candidates_dir=args.candidate_dir,
            markers=markers,
            require_all_markers=args.require_all_markers,
        )
        print(root)
        return

    if args.command == "init-config":
        markers = tuple(args.marker)
        output = Path(args.output)
        if output.exists() and not args.force:
            raise FileExistsError(
                f"{output} already exists. Use --force to overwrite."
            )
        text = render_config_template(
            candidates_dir=args.candidate_dir,
            markers=markers,
        )
        output.write_text(text, encoding="utf-8")
        print(f"Wrote {output}")


if __name__ == "__main__":
    main()
