"""Manage IO for GAM project files."""
from pathlib import Path

import tomlkit
from tomlkit import parse

from gamcore.models import GAMProject

__all__ = ("ProjectHandler",)
latest_supported_godot = "3.4.2"


class ProjectHandler:
    """Handle GAM project config files and operations."""

    def __init__(self, path: Path | str, details: GAMProject | None = None) -> None:
        self.path: Path = Path(path)
        self.details: GAMProject | None = details
        if self.details:
            self._save()
        else:
            self._load()

    @staticmethod
    def new(path: Path | str, name: str) -> "ProjectHandler":
        """Create a new GAM project.

        :param path: Path to create new project in.
        :param name: Name of the new GAM project.
        """
        details = GAMProject(
            name=name,
            version="0.1.0",
            godot_version=latest_supported_godot,
            source_directory="src",
            packages=["src"],
        )
        return ProjectHandler(path, details=details)

    def _save(self) -> None:
        toml = tomlkit.dumps({"gamproject": self.details.dict(exclude_unset=True)})
        self.path.joinpath("gamproject.toml").write_text(toml)

    def _load(self) -> None:
        toml_file = self.path.joinpath("gamproject.toml")
        if not toml_file.exists():
            raise FileNotFoundError()
        details = GAMProject(
            **{**parse(toml_file.read_text())["gamproject"], **{"path": self.path}}
        )
        self.details = details
