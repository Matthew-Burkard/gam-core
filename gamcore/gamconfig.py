"""Manage IO to a GAM config file."""
import os
from pathlib import Path

import tomlkit


class GAMConfig:
    """GAM config variables."""

    __instance__: "GAMConfig" = None

    def __init__(self, path: Path | None = None) -> None:
        if GAMConfig.__instance__ is not None:
            raise AssertionError("Instance of singleton GAMConfig already exists.")
        self._path: Path = path or Path.home().joinpath(".config/gam/config.toml")
        self._cache_dir: str = (Path.home() / ".cache/gam").as_posix()
        if not self.cache_dir.exists():
            self.cache_dir.mkdir()
        if not self._path.parent.exists():
            os.makedirs(self._path.parent)
        self.repositories: list[str] = []
        if self._path.exists():
            self.load()
        else:
            self.save()

    @property
    def cache_dir(self) -> Path:
        """The GAM cache directory for installed packages."""
        return (
            Path(self._cache_dir)
            if self._cache_dir.startswith("/")
            else self._path.parent / self._cache_dir
        )

    @cache_dir.setter
    def cache_dir(self, cache_dir: Path | str) -> None:
        if cache_dir.resolve() != self.cache_dir.resolve():
            self._cache_dir = cache_dir.as_posix()

    @property
    def path(self) -> Path:
        """Path to "config.toml" file."""
        return self._path

    @path.setter
    def path(self, path: Path) -> None:
        self._path = path
        self.load()

    @staticmethod
    def get_instance(path: Path | None = None) -> "GAMConfig":
        """Get the instance of GAMConfig.

        If it does not already exist it will be created.
        """
        if GAMConfig.__instance__ is not None:
            if path is not None:
                GAMConfig.__instance__.path = path
            return GAMConfig.__instance__
        instance = GAMConfig(path)
        GAMConfig.__instance__ = instance
        return instance

    def save(self) -> None:
        """Save a GAM config file."""
        gam_dict = {
            "gam": {
                "cache_dir": self._cache_dir,
                "repositories": self.repositories,
            }
        }
        if not self._path.exists():
            self._path.touch()
        self._path.write_text(tomlkit.dumps(gam_dict))

    def load(self) -> None:
        """Load values from config file at path."""
        gam = tomlkit.parse(self._path.read_text())["gam"]
        self._cache_dir = gam.get("cache_dir")
        # Make path absolute if it's relative.
        self.repositories = gam.get("repositories") or []
