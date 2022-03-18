"""Handles requirement installation."""
import os
import shutil
import tarfile
import uuid
from pathlib import Path

from gamcore.gamconfig import GAMConfig
from gamcore.handlers.project import ProjectHandler
from gamcore.handlers.requirement import RequirementHandler, RequirementSourceType


class InstallHandler:
    """Handle the installation of a package in a GAM project."""

    def __init__(self, path: Path | str, requirement: RequirementHandler) -> None:
        self.path = path
        self.requirement = requirement

    def execute(self) -> bool:
        """Install the requirement into the project."""
        match self.requirement.source:
            case RequirementSourceType.FILE:
                return self._install_from_file()

    def _install_from_file(self) -> bool:
        filepath = Path(self.requirement.filepath)
        tmp_dir = GAMConfig.get_instance().tmp_dir.joinpath(str(uuid.uuid4()))
        # Unzip tarball to package_tmp.
        tar = tarfile.open(filepath)
        tar.extractall(tmp_dir)
        tar.close()
        self._install(tmp_dir.joinpath(filepath.name.removesuffix(".tar.gz")))
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return True

    def _install(self, project_path: Path | str) -> None:
        target_project = ProjectHandler(project_path)
        pkg_name = f"{target_project.details.name}-{target_project.details.version}"
        pkg_artifact_path = GAMConfig.get_instance().cache_dir.joinpath(
            f"artifacts/{pkg_name}"
        )
        # Remove artifact if it already exists.
        shutil.rmtree(pkg_artifact_path, ignore_errors=True)
        shutil.copytree(project_path, pkg_artifact_path)
        addons_path = Path(self.path).joinpath("addons")
        addons_path.mkdir(exist_ok=True)
        install_path = addons_path.joinpath(target_project.details.name)
        # Remove existing installation of this package if it exists.
        if install_path.is_symlink():
            os.remove(install_path)
        os.symlink(pkg_artifact_path, install_path, target_is_directory=True)

    def _install_from_git(self) -> None:
        pass

    def _install_from_url(self) -> None:
        pass

    def _install_from_repository(self) -> None:
        pass
