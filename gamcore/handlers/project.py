"""Manage IO for GAM project files."""
import os
import shutil
import tarfile
from pathlib import Path

import tomlkit

from gamcore.models import GAMProject
from gamcore.templates.godot_project_file import project_file

__all__ = ("ProjectHandler",)
latest_supported_godot = ">=4.0"


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
            packages=["**/*"],
        )
        project_root = Path(path).joinpath(name)
        if project_root.exists():
            raise FileExistsError(f"{project_root.as_posix()} already exists.")
        project_root.mkdir()
        project_root.joinpath("src").mkdir()
        godot_project_file = project_root / "project.godot"
        godot_project_file.touch()
        godot_project_file.write_text(project_file.format(name=name))
        return ProjectHandler(project_root, details=details)

    def build(self) -> Path:
        """Build the GAM project into a distributable tarball.

        :return: The path to the tarball.
        """
        # Remove existing build and create directories.
        dist_path = self.path / "dist"
        package_path = dist_path.joinpath(f"{self.details.name}-{self.details.version}")
        shutil.rmtree(package_path, ignore_errors=True)
        os.makedirs(package_path, exist_ok=True)
        # For each glob, copy matching files and directories.
        for glob in self.details.packages:
            source_path = Path(self.path).joinpath(self.details.source_directory)
            for path in source_path.glob(glob):
                dest = path.as_posix().removeprefix(f"{source_path.as_posix()}/")
                if Path(path).is_dir():
                    shutil.copytree(path, package_path.joinpath(dest))
                else:
                    os.makedirs(package_path.joinpath(dest).parent, exist_ok=True)
                    shutil.copyfile(path, package_path.joinpath(dest))
        shutil.copyfile(
            self.path.joinpath("gamproject.toml"),
            package_path.joinpath("gamproject.toml"),
        )
        # Make tarball.
        tarball_path = dist_path.joinpath(
            f"{self.details.name}-{self.details.version}.tar.gz"
        )
        _make_tarfile(str(package_path), str(tarball_path))
        return tarball_path

    def get_installed_version(self, name: str) -> str | None:
        """Get the currently installed version of a package."""
        dep_path = self.path.joinpath(f"addons/{name}")
        if not dep_path.is_dir():
            return None
        return tomlkit.parse(dep_path.joinpath("gamproject.toml").read_text())[
            "gamproject"
        ]["version"]

    def _save(self) -> None:
        toml = tomlkit.dumps({"gamproject": self.details.dict(exclude_unset=True)})
        self.path.joinpath("gamproject.toml").write_text(toml)

    def _load(self) -> None:
        toml_file = self.path.joinpath("gamproject.toml")
        if not toml_file.exists():
            raise FileNotFoundError()
        details = GAMProject(
            **{
                **tomlkit.parse(toml_file.read_text())["gamproject"],
                **{"path": self.path},
            }
        )
        self.details = details


def _make_tarfile(source_dir: str, output_filename: str) -> None:
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
