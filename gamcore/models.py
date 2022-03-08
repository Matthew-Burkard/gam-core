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


class PackageSource(BaseModel):
    """Describes the source of a package."""

    type: str
    url: str | None
    reference: str | None
    resolved_references: str | None


class Package(BaseModel):
    """Represents an installed package."""

    dependencies: dict[str, str]
    source: PackageSource | None = None
