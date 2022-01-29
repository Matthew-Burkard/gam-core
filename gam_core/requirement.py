"""Manage requirements data."""
import re
from enum import auto, Enum
from pathlib import Path


class RequirementSourceType(Enum):
    """The source of any given requirement."""

    FILE = auto()
    GIT = auto()
    REPOSITORY = auto()
    URL = auto()


class Requirement:
    """Represents a GAM project requirement."""

    def __init__(self, requirement_string: str):
        self.requirement_string = requirement_string
        if self._is_filepath():
            self.source = RequirementSourceType.FILE
        elif self._is_url():
            self.source = RequirementSourceType.URL
        elif self._is_git():
            self.source = RequirementSourceType.GIT
        elif self._is_in_repository():
            self.source = RequirementSourceType.REPOSITORY
        else:
            raise ValueError(f"Cannot find {requirement_string} in any source.")

    def _is_filepath(self) -> bool:
        return (
            Path(self.requirement_string).is_file()
            or Path.cwd().joinpath(self.requirement_string).is_file()
        )

    def _is_git(self) -> bool:
        return False  # TODO

    def _is_in_repository(self) -> bool:
        return False  # TODO

    def _is_url(self) -> bool:
        if bool(re.match(r"^https?://", self.requirement_string)):
            pass  # TODO
        return False
