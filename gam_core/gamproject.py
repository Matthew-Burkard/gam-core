"""Provides GAMProject properties definition."""
from pydantic import BaseModel, Field


class GAMProject(BaseModel):
    """Dataclass for GAM project properties."""

    name: str
    version: str
    godot_version: str
    packages: list[str] = Field(default=lambda: [])
    description: str | None
    repository: str | None
    homepage: str | None
    license: str | None
    authors: list[str] | None
    dependencies: dict[str, str] | None
    dev_dependencies: dict[str, str] | None
