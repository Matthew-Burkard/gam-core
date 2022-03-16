"""Repository util functions."""
import os
from pathlib import Path

from gamcore.handlers.project import ProjectHandler
from gamcore.models import GAMProject


def get_installed_packages(path: Path | str) -> list[GAMProject]:
    """Get all installed packages for this project."""
    projects = []
    addons = path / "addons"
    if not addons.exists():
        return []
    for directory in os.listdir(addons):
        installed_project = Path(addons / directory)
        if installed_project.joinpath("gamproject.toml").is_file():
            projects.append(ProjectHandler(installed_project).details)
    return projects
