"""Manage IO for GAM project files."""
from pathlib import Path

from tomlkit import parse

from gamcore.models import GAMProject


def load(path: Path | str) -> GAMProject:
    """Load GAM project details.

    :param path: Path to GAM project root.
    :return: The project details.
    """
    path = Path(path)
    toml_file = path.joinpath("gamproject.toml")
    if not toml_file.exists():
        raise FileNotFoundError()
    details = GAMProject(
        **{**parse(toml_file.read_text())["gamproject"], **{"path": path}}
    )
    return details
