"""Provides class exposing GAM core functionality."""
import logging
import re
from pathlib import Path

from gam_core import _gamconfig, _projectconfig

__all__ = ("GAMCore",)

from gam_core._build import build

log = logging.getLogger(__name__)


class GAMCore:
    """Class containing GAM functionality."""

    def __init__(
        self,
        config_dir: Path | str | None = None,
        cache_path: Path | str | None = None,
    ) -> None:
        cache_dir = Path.home() / ".cache" / "gam"
        artifacts = cache_dir / "artifacts"
        tmp = cache_dir / "tmp"
        config_dir.mkdir(exist_ok=True)
        cache_path.mkdir(exist_ok=True)
        self.config = _gamconfig.get_config(config_dir)

    @staticmethod
    def new(path: str) -> None:
        """Create a new GAM project at the given path.

        :param path: Path to new project.
        """
        if re.match(r"^(../|./|/)", path):
            name = re.search(r"(?<=/)(.*($|/$))", path)
            path = Path(path)
        else:
            name = path
            path = Path.cwd().joinpath(path)
        path.mkdir()
        _projectconfig.new(path, name)

    @staticmethod
    def build(self, path: str) -> None:
        """Build a Godot project into a distributable tarball."""
        build(path)
