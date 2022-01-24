"""Provides class exposing GAM core functionality."""
import logging
import re
from pathlib import Path

from gam_core import _gamconfig, _projectconfig
from gam_core._add import AddHandler
from gam_core._build import build

__all__ = ("GAMCore",)

log = logging.getLogger(__name__)


class GAMCore:
    """Class containing GAM functionality."""

    def __init__(
        self,
        config_dir: Path | str | None = None,
    ) -> None:
        self.config = _gamconfig.get_config(config_dir / "config.toml")
        self.config.cache_dir.mkdir(exist_ok=True)
        self.config.artifacts_dir.mkdir(exist_ok=True)

    def add(
        self, path: Path | str, name: str, required: bool = True, dev: bool = False
    ) -> None:
        """Add a dependency to a Godot project."""
        # TODO Check for constraint.
        #  e.g. selections@^0.8.5
        #  e.g. "selections>=0.8.5"
        # TODO Check lockfile fo version to use.
        handler = AddHandler(self.config, _projectconfig.load(path))
        new_dependency = handler.add(name)
        # TODO Update lockfile.

    @staticmethod
    def build(path: Path | str) -> Path:
        """Build a Godot project into a distributable tarball."""
        return build(_projectconfig.load(path))

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
