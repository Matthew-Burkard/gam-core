"""Manage IO to a GAM config file."""
from pathlib import Path

from pydantic import BaseModel, Field
from tomlkit import dumps, parse


class GAMConfig(BaseModel):
    """GAM config variables."""

    cache_dir: str = Field(
        default=lambda: Path.home().joinpath("/.cache/gam").as_posix()
    )
    repositories: list[str] = Field(default=lambda: [])


def load(path: str | Path | None) -> GAMConfig:
    """Get a GAM config object from a file."""
    path = Path(path) if path else Path.home().joinpath("./config/gam/")
    return GAMConfig(**parse(path.read_text())["gam"])


def save(path: str | Path | None, config: GAMConfig | None) -> None:
    """Save a GAM config file."""
    path = Path(path) if path else Path.home().joinpath("./config/gam/")
    config = config or GAMConfig()
    path.write_text(dumps({"gam": config.dict(exclude_unset=True)}))
