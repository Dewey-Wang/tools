"""Portable project-root path utilities."""

from .root import project_path, resolve_project_root
from .template import render_config_template

__all__ = ["resolve_project_root", "project_path", "render_config_template"]
