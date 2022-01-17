"""Provides data class describing a dependency."""
from pydantic import BaseModel


class Dependency(BaseModel):
    """A dependency of a project."""
    name: str
    version: str
    optional: bool
    description: str | None
