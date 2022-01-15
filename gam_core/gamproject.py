"""Provides GAMProject properties definition."""
from typing import Optional

from pydantic import BaseModel


class GAMProject(BaseModel):
    """Dataclass for GAM project properties."""
    name: str
    version: str
    description: Optional[str]
    repository: Optional[str]
    homepage: Optional[str]
    license: Optional[str]
    authors: Optional[list[str]]
    dependencies: Optional[dict[str, str]]
    dev_dependencies: Optional[dict[str, str]]
    godot_version: str
