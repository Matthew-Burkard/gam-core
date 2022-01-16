"""Build a Godot asset into a distributable package."""
import os
import shutil
import tarfile
from pathlib import Path

from gam_core import _projectconfig


def build(root_dir: Path | str) -> Path:
    """Package a Godot asset into a distributable package.

    :param root_dir: Root directory of a GAM project.
    :return: Path to the generated tarball.
    """
    # Remove existing build and create directories.
    root_dir = Path(root_dir)
    config = _projectconfig.load(root_dir)
    dist_path = root_dir / "dist"
    package_path = dist_path.joinpath(f"{config.name}-{config.version}")
    shutil.rmtree(package_path, ignore_errors=True)
    os.makedirs(package_path, exist_ok=True)
    # For each glob, copy matching files and directories.
    for glob in config.packages:
        for path in Path(root_dir).glob(glob):
            dest = path.as_posix().removeprefix(root_dir.as_posix()).removeprefix("/")
            if Path(path).is_dir():
                os.makedirs(dest, exist_ok=True)
                shutil.copytree(path, package_path.joinpath(dest))
            else:
                os.makedirs(package_path.joinpath(dest).parent, exist_ok=True)
                shutil.copyfile(path, package_path.joinpath(dest))
    # Make tarball.
    tarball_path = dist_path.joinpath(f"{config.name}-{config.version}.tar.gz")
    _make_tarfile(str(package_path), str(tarball_path))
    return tarball_path


def _make_tarfile(source_dir: str, output_filename: str) -> None:
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
