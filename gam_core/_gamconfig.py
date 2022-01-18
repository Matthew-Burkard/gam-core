"""Manage IO to a GAM config file."""
from pathlib import Path

from pydantic import BaseModel, Field
from tomlkit import dumps, parse


class GAMConfig(BaseModel):
    """GAM config variables."""

    cache_dir: Path = Field(default=lambda: Path.home().joinpath("/.cache/gam"))
    repositories: list[str] = Field(default=lambda: [])


def get_config(path: Path | str | None) -> GAMConfig:
    """Get a GAM config object from a file or make a new one."""
    path = Path(path) if path else Path.home().joinpath("./config/gam/config.toml")
    if path.exists():
        return _load(path)
    config = GAMConfig()
    save(path, config)
    return config


def save(path: Path | str | None, config: GAMConfig | None) -> None:
    """Save a GAM config file."""
    path = Path(path) if path else Path.home().joinpath("./config/gam/config.toml")
    config = config or GAMConfig()
    path.write_text(dumps({"gam": config.dict(exclude_unset=True)}))


def _load(path: Path | str) -> GAMConfig:
    return GAMConfig(**parse(path.read_text())["gam"])
