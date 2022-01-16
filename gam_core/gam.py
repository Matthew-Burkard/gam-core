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
        cache_dir: Path | str | None = None,
    ) -> None:
        cache_dir = cache_dir or Path.home() / ".cache" / "gam"
        cache_dir.mkdir(exist_ok=True)
        artifacts = cache_dir / "artifacts"
        artifacts.mkdir(exist_ok=True)
        config_dir.mkdir(exist_ok=True)
        cache_dir.mkdir(exist_ok=True)
        self.config = _gamconfig.get_config(config_dir / "config.toml")

    @staticmethod
    def new(path: Path | str) -> None:
        """Create a new GAM project at the given path.

        :param path: Path to new project.
        """
        if re.match(r"^(../|./|/)", path):
            name = re.search(r"(?<=/)([^/]+($|/$))", path).group(1)
            path = Path(path)
        else:
            name = path
            path = Path.cwd().joinpath(path)
        path.mkdir()
        _projectconfig.new(path, name)

    @staticmethod
    def build(path: Path | str) -> None:
        """Build a Godot project into a distributable tarball."""
        build(path)
