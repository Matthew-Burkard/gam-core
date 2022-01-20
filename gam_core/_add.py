"""Install a Godot asset."""
import re
import tarfile
import uuid
from pathlib import Path

from gam_core import _projectconfig
from gam_core._gamconfig import GAMConfig
from gam_core.gamproject import GAMProject


class AddHandler:
    """Class to manage adding a dependency to a project."""

    def __init__(self, gam_config: GAMConfig, project_config: GAMProject) -> None:
        self.gam_config = gam_config
        self.gam_project = project_config

    def add(self, name: str) -> GAMProject:
        """Add a dependency to a GAM project.

        :param name: Name of the dependency to add.
        :return: The details of the dependency.
        """

        if _is_filepath(name):
            return self._add_from_file(name)
        if _in_repositories(name):
            return self._add_from_repository(name)
        if _is_url(name):
            if _is_git_repository(name):
                return self._add_from_git(name)
            else:
                return self._add_from_url(name)
        raise ValueError(f"Could not find a matching version of package {name}")

    def _add_from_file(self, path: str) -> GAMProject:
        uid = str(uuid.uuid4())
        tmp_dir = self.gam_config.cache_dir.joinpath("tmp")
        tmp_dir.mkdir(exist_ok=True)
        tmp_pkg_dir = tmp_dir.joinpath(uid)
        tmp_pkg_dir.mkdir(exist_ok=True)
        _unzip_tar(path, tmp_pkg_dir)
        project_config = _projectconfig.load(tmp_pkg_dir)
        # TODO Add to cache.
        # TODO Symlink artifact to self.gam_project.path.joinpath("addons")
        return project_config

    def _add_from_repository(self, name: str) -> GAMProject:
        pass

    def _add_from_git(self, url: str) -> GAMProject:
        pass

    def _add_from_url(self, url: str) -> GAMProject:
        pass


def _is_url(name: str) -> bool:
    return bool(re.match(r"^https?://", name))


def _is_git_repository(name: str) -> bool:
    return False  # TODO


def _is_filepath(name: str) -> bool:
    is_file = Path(name).is_file() or Path.cwd().joinpath(name).is_file()
    return is_file and re.match(r"\.tar\.gz$", name)


def _in_repositories(name: str) -> bool:
    return False  # TODO


def _unzip_tar(tar_path: Path | str, target_path: Path | str) -> None:
    tar = tarfile.open(tar_path)
    tar.extractall(target_path)
    tar.close()
