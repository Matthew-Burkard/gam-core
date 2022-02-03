"""Manage requirements data."""
import os
import re
import tarfile
import uuid
from enum import auto, Enum
from pathlib import Path

from gam_core import project
from gam_core.gamconfig import GAMConfig
from gam_core.gamproject import GAMProjectDetails


class RequirementSourceType(Enum):
    """The source of any given requirement."""

    FILE = auto()
    GIT = auto()
    REPOSITORY = auto()
    URL = auto()


class Requirement:
    """Represents a GAM project requirement."""

    def __init__(self, requirement_string: str):
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
        self._project_details: GAMProjectDetails | None = None

    @property
    def project_details(self) -> GAMProjectDetails:
        """The project details for this requirement."""
        if self._project_details is None:
            match self.source:
                case RequirementSourceType.FILE:
                    self._project_details = self._get_details_from_file()
                case RequirementSourceType.FILE:
                    self._project_details = self._get_details_from_git()
                case RequirementSourceType.FILE:
                    self._project_details = self._get_details_from_repository()
                case RequirementSourceType.FILE:
                    self._project_details = self._get_details_from_url()
        return self._project_details

    def _get_details_from_file(self) -> GAMProjectDetails:
        uid = str(uuid.uuid4())
        tmp_dir = GAMConfig.get_instance().cache_dir.joinpath("tmp")
        tmp_dir.mkdir(exist_ok=True)
        tmp_pkg_dir = tmp_dir.joinpath(uid)
        tmp_pkg_dir.mkdir(exist_ok=True)
        _unzip_tar(self.requirement_string, tmp_pkg_dir)
        # Search content of tmp_pkg_dir to get extracted directory name.
        unpacked_pkg_dir = None
        for path, directories, files in os.walk(tmp_pkg_dir):
            if len(directories) != 1:
                raise ValueError(f"File not recognized as GAM tarball at {path}")
            unpacked_pkg_dir = tmp_pkg_dir / directories[0]
            break
        # Load GAM project details of added package.
        return project.load(unpacked_pkg_dir).details

    def _get_details_from_git(self) -> GAMProjectDetails:
        pass  # TODO

    def _get_details_from_repository(self) -> GAMProjectDetails:
        pass  # TODO

    def _get_details_from_url(self) -> GAMProjectDetails:
        pass  # TODO

    def _is_filepath(self) -> bool:
        return (
            Path(self.requirement_string).is_file()
            or Path.cwd().joinpath(self.requirement_string).is_file()
        )

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
