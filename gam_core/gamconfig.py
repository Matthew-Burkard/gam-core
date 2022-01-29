"""Manage IO to a GAM config file."""
from pathlib import Path

from tomlkit import dumps, parse


class GAMConfig:
    """GAM config variables."""

    __instance__ = None

    def __init__(self, path: Path) -> None:
        if GAMConfig.__instance__ is not None:
            raise AssertionError("Instance of singleton GAMConfig already exists.")
        self.path: Path = path
        gam = _load(self.path)
        self.cache_dir: Path = gam.get("cache_dir") or (Path.home() / ".cache/gam")
        self.repositories: list[str] = gam.get("repositories") or []

    @staticmethod
    def get_instance() -> "GAMConfig":
        """Get the instance of GAMConfig.

        If it does not already exist it will be created.
        """
        if GAMConfig.__instance__ is not None:
            return GAMConfig.__instance__
        return GAMConfig(Path.home().joinpath("./config/gam/config.toml"))

    def save(self) -> None:
        """Save a GAM config file."""
        gam_dict = {
            "gam": {
                "cache_dir": self.cache_dir,
                "repositories": self.repositories,
            }
        }
        self.path.write_text(dumps(gam_dict))


def _load(path: Path | str) -> dict:
    return parse(path.read_text())["gam"]
