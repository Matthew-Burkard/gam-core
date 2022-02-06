"""GAM core functions"""
from pathlib import Path

from models import GAMProject


def build(path: Path | str) -> Path:
    """Build the GAM project at the given path.

    :param path: A GAM project root directory.
    :return: Path to the build tarball.
    """
    pass


def add(path: Path | str, requirement_string: str) -> GAMProject:
    """Add a requirement to a GAM project.

    :param path:
    :param requirement_string:
    :return: Details of the added requirement.
    """
    pass
