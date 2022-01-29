"""Provides GAMProject properties definition."""
from pathlib import Path

from pydantic import BaseModel, Field


class GAMProjectDetails(BaseModel):
    """Dataclass for GAM project configuration details."""

    name: str
    version: str
    godot_version: str
    source_directory: str
    packages: list[str] = Field(default=lambda: [])
    description: str | None = None
    repository: str | None = None
    homepage: str | None = None
    license: str | None = None
    authors: list[str] = Field(default=lambda: [])
    dependencies: list[str] = Field(default=lambda: [])
    dev_dependencies: list[str] = Field(default=lambda: [])


class GAMLock(BaseModel):
    """Holds GAM lock file contents."""

    packages: list[GAMProjectDetails] = Field(default=lambda: [])


class GAMProject(BaseModel):
    """Holds GAM project properties."""

    details: GAMProjectDetails
    installed: list[GAMProjectDetails] = Field(default_factory=lambda: [])
    lock: GAMLock
    path: Path
