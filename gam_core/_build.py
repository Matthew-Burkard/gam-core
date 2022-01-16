"""Build a Godot asset into a distributable package."""
import logging
import os
import shutil
import tarfile
from pathlib import Path

from gam_core import _projectconfig

__all__ = ("build",)

log = logging.getLogger(__name__)


def build(root_dir: Path | str) -> Path:
    """Package a Godot asset into a distributable package."""
    root_dir = Path(root_dir)
    config = _projectconfig.load(root_dir)
    dist_path = root_dir / "dist"
    package_path = dist_path.joinpath(f"{config.name}-{config.version}")
    for path in config.packages:
        shutil.copytree(path, package_path.joinpath(path))
    tarball_path = dist_path.joinpath(f"{config.name}-{config.version}.tar.gz")
    _make_tarfile(str(package_path), str(tarball_path))
    return tarball_path


def _make_tarfile(source_dir: str, output_filename: str) -> None:
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
