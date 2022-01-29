"""Handles requirement installation."""
import os
import shutil
from pathlib import Path

from gam_core._gamconfig import GAMConfig
from gam_core.gamproject import GAMProject, GAMProjectDetails
from gam_core.requirement import Requirement, RequirementSourceType


class InstallHandler:
    """Class to handle the installation of a requirement."""

    def __init__(
        self, gam_config: GAMConfig, gam_project: GAMProject, requirement: Requirement
    ) -> None:
        self._gam_config = gam_config
        self._gam_project = gam_project
        self._requirement = requirement

    def install(self) -> bool:
        """Install the requirement into the project."""
        match self._requirement.source:
            case RequirementSourceType.FILE:
                return self._install_from_file()
            case RequirementSourceType.FILE:
                return self._install_from_git()
            case RequirementSourceType.FILE:
                return self._install_from_repository()
            case RequirementSourceType.FILE:
                return self._install_from_url()

    def _install_from_file(self) -> bool:
        pass

    def _install_from_git(self) -> bool:
        pass

    def _install_from_url(self) -> bool:
        pass

    def _install_from_repository(self) -> bool:
        pass

    def _install(self, project: GAMProjectDetails) -> None:
        pkg_name = f"{project.name}-{project.version}"
        pkg_artifact_path = self._gam_config.cache_dir.joinpath(f"artifacts/{pkg_name}")
        # Remove artifact if it already exists.
        shutil.rmtree(pkg_artifact_path, ignore_errors=True)
        shutil.move(GAMProject.path, pkg_artifact_path)
        addons_path = Path(self._gam_project.path).joinpath("addons")
        addons_path.mkdir(exist_ok=True)
        install_path = addons_path.joinpath(project.name)
        # Remove existing installation of this package if it exists.
        if install_path.is_symlink():
            os.remove(install_path)
        os.symlink(pkg_artifact_path, install_path, target_is_directory=True)
