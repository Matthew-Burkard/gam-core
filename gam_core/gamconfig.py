"""Manage IO to a GAM config file."""
from pathlib import Path

from pydantic import BaseModel, Field


class GAMConfig(BaseModel):
    """GAM config variables."""

    cache_dir: str = Field(
        default=lambda: Path.home().joinpath("/.cache/gam").as_posix()
    )
    repositories: list[str] = Field(default=lambda: [])
