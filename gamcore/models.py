"""GAM models."""
from pydantic import BaseModel, Field


class GAMProject(BaseModel):
    """Dataclass for GAM project configuration details."""

    name: str
    version: str
    godot_version: str
    source_directory: str
    packages: list[str] = Field(default_factory=lambda: [])
    description: str | None = None
    repository: str | None = None
    homepage: str | None = None
    license: str | None = None
    authors: list[str] = Field(default_factory=lambda: [])
    dependencies: dict[str, str] = Field(default_factory=lambda: {})
    dev_dependencies: dict[str, str] = Field(default_factory=lambda: {})
