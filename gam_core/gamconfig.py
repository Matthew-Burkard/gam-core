"""Manage IO to a GAM config file."""
from pathlib import Path

from tomlkit import dumps, parse


class GAMConfig:
    """GAM config variables."""

    __instance__ = None

    def __init__(self) -> None:
        if GAMConfig.__instance__ is not None:
            raise AssertionError("Instance of singleton GAMConfig already exists.")
        self._path: Path = Path.home().joinpath("./config/gam/config.toml")
        self.cache_dir: Path = (Path.home() / ".cache/gam")
        self.repositories: list[str] = []
        self.load()

    @property
    def path(self) -> Path:
        """Path to "config.toml" file."""
        return self._path

    @path.setter
    def path(self, p: Path) -> None:
        self._path = p
        self.load()

    @staticmethod
    def get_instance() -> "GAMConfig":
        """Get the instance of GAMConfig.

        If it does not already exist it will be created.
        """
        if GAMConfig.__instance__ is not None:
            return GAMConfig.__instance__
        return GAMConfig()

    def save(self) -> None:
        """Save a GAM config file."""
        gam_dict = {
            "gam": {
                "cache_dir": self.cache_dir,
                "repositories": self.repositories,
            }
        }
        self._path.write_text(dumps(gam_dict))

    def load(self) -> None:
        """Load values from config file at path,"""
        gam = parse(self._path.read_text())["gam"]
        self.cache_dir = gam.get("cache_dir")
        self.repositories = gam.get("repositories")
