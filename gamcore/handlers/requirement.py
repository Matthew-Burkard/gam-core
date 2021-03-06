"""Manage requirements data."""
import os
import re
import shutil
import tarfile
import uuid
from enum import auto, Enum
from pathlib import Path

from gamcore.gamconfig import GAMConfig
from gamcore.models import GAMProject
from gamcore.handlers.project import ProjectHandler


class RequirementSourceType(Enum):
    """The source of any given requirement."""

    FILE = auto()
    GIT = auto()
    REPOSITORY = auto()
    URL = auto()


class RequirementHandler:
    """Represents a GAM project requirement."""

    def __init__(self, requirement_string: str):
        self.filepath: str | None = None
        self._name: str | None = None
        self._version_rule: str | None = None
        if "@" in requirement_string:
            self._name, self._version_rule = requirement_string.split("@")
        self.requirement_string = requirement_string
        if self._is_filepath():
            self.source = RequirementSourceType.FILE
        elif self._is_git():
            self.source = RequirementSourceType.GIT
        elif self._is_in_repository():
            self.source = RequirementSourceType.REPOSITORY
        elif self._is_url():
            self.source = RequirementSourceType.URL
        else:
            raise ValueError(f"Cannot find {requirement_string} in any source.")
        self._project_details: GAMProject | None = None

    @property
    def project_details(self) -> GAMProject:
        """The project details for this requirement."""
        # TODO When lock files is thing, search there first.
        if self._project_details is None:
            match self.source:
                case RequirementSourceType.FILE:
                    self._project_details = self._get_details_from_file()
                case RequirementSourceType.GIT:
                    self._project_details = self._get_details_from_git()
                case RequirementSourceType.REPOSITORY:
                    self._project_details = self._get_details_from_repository()
                case RequirementSourceType.URL:
                    self._project_details = self._get_details_from_url()
        return self._project_details

    @property
    def version_rule(self) -> str:
        """The version rule of this requirement."""
        if self._version_rule is not None:
            return self._version_rule
        return f"^{self.project_details.version}"

    def _get_details_from_file(self) -> GAMProject:
        uid = str(uuid.uuid4())
        tmp_dir = GAMConfig.get_instance().tmp_dir
        tmp_pkg_dir = tmp_dir.joinpath(uid)
        tmp_pkg_dir.mkdir(exist_ok=True)
        _unzip_tar(self.filepath, tmp_pkg_dir)
        # Search content of tmp_pkg_dir to get extracted directory name.
        unpacked_pkg_dir = None
        for path, directories, files in os.walk(tmp_pkg_dir):
            if len(directories) != 1:
                raise ValueError(f"File not recognized as GAM tarball at {path}")
            unpacked_pkg_dir = tmp_pkg_dir / directories[0]
            break
        # Load GAM project details of added package.
        project = ProjectHandler(unpacked_pkg_dir)
        shutil.rmtree(tmp_pkg_dir)
        return project.details

    def _get_details_from_git(self) -> GAMProject:
        pass  # TODO

    def _get_details_from_repository(self) -> GAMProject:
        pass  # TODO

    def _get_details_from_url(self) -> GAMProject:
        pass  # TODO

    def _is_filepath(self) -> bool:
        if self._version_rule is not None:
            if Path(self._version_rule).is_file():
                self.filepath = self._version_rule
                return True
            if Path.cwd().joinpath(self._version_rule).is_file():
                self.filepath = Path.cwd().joinpath(self._version_rule)
                return True
        if Path(self.requirement_string).is_file():
            self.filepath = Path(self.requirement_string)
            return True
        if Path.cwd().joinpath(self.requirement_string).is_file():
            self.filepath = Path.cwd().joinpath(self.requirement_string)
            return True
        return False

    def _is_git(self) -> bool:
        pass  # TODO

    def _is_in_repository(self) -> bool:
        pass  # TODO

    def _is_url(self) -> bool:
        if bool(re.match(r"^https?://", self.requirement_string)):
            pass  # TODO
        return False


def _unzip_tar(tar_path: Path | str, target_path: Path | str) -> None:
    tar = tarfile.open(tar_path)
    tar.extractall(target_path)
    tar.close()
