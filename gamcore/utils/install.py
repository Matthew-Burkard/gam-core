"""Handles requirement installation."""
import os
import shutil
from pathlib import Path

from gamcore.gamconfig import GAMConfig
from gamcore.utils import project
from gamcore.utils.requirement import Requirement, RequirementSourceType


def install(project_path: Path | str, requirement: Requirement) -> bool:
    """Install the requirement into the project."""
    match requirement.source:
        case RequirementSourceType.FILE:
            return _install_from_file()
        case RequirementSourceType.FILE:
            return _install_from_git()
        case RequirementSourceType.FILE:
            return _install_from_repository()
        case RequirementSourceType.FILE:
            return _install_from_url()


def _install_from_file(project_path: Path | str, tarball_path: Path | str) -> bool:
    # TODO Copy tarball to tmp.
    pkg_artifact_path = GAMConfig.get_instance().tmp
    shutil.copytree()
    # TODO Unzip tarball to package_tmp.
    package_tmp = "TODO"
    # TODO _install(project_path, package_tmp).
    shutil.rmtree(package_tmp, ignore_errors=True)
    return True


def _install_from_git() -> bool:
    pass


def _install_from_url() -> bool:
    pass


def _install_from_repository() -> bool:
    pass


def _install(project_path: Path | str, target_path: Path | str) -> None:
    target_project = project.load(target_path)
    pkg_name = f"{target_project.name}-{target_project.version}"
    pkg_artifact_path = GAMConfig.get_instance().cache_dir.joinpath(
        f"artifacts/{pkg_name}"
    )
    # Remove artifact if it already exists.
    shutil.rmtree(pkg_artifact_path, ignore_errors=True)
    shutil.copytree(target_path, pkg_artifact_path)
    addons_path = Path(project_path).joinpath("addons")
    addons_path.mkdir(exist_ok=True)
    install_path = addons_path.joinpath(target_project.name)
    # Remove existing installation of this package if it exists.
    if install_path.is_symlink():
        os.remove(install_path)
    os.symlink(pkg_artifact_path, install_path, target_is_directory=True)
