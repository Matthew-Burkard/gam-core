"""Manage IO to a GAM project config file."""
from pathlib import Path

from tomlkit import dumps, parse
from gam_core.gamproject import GAMProject

_latest_stable_godot_version = "3.4.2"


def new(root_dir: Path | str, name: str, godot_version: str | None = None) -> None:
    """Create a new "gamproject.toml" file."""
    gamproject = GAMProject(
        name=name,
        version="0.1.0",
        source_directory=f"addons/{name}",
        godot_version=godot_version or _latest_stable_godot_version,
        path=root_dir,
    )
    _save(root_dir, gamproject)


def load(project_root: Path | str) -> GAMProject:
    """Get the GAMProject information from a project root dir."""
    toml_file = Path(project_root).joinpath("gamproject.toml")
    if not toml_file.exists():
        raise FileNotFoundError()
    return GAMProject(
        **{**parse(toml_file.read_text())["gamproject"], **{"path": project_root}}
    )


def _save(project_root: Path | str, gamproject: GAMProject) -> None:
    toml = dumps({"gamproject": gamproject.dict(exclude_unset=True)})
    Path(project_root).joinpath("gamproject.toml").write_text(toml)
