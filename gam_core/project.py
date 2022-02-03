"""Manage IO to a GAM project config file."""
from pathlib import Path

from tomlkit import dumps, parse
from gam_core.gamproject import GAMLock, GAMProject, GAMProjectDetails

_latest_stable_godot_version = "3.4.2"


def new(root_dir: Path | str, name: str, godot_version: str | None = None) -> None:
    """Create a new "gamproject.toml" file."""
    details = GAMProjectDetails(
        name=name,
        version="0.1.0",
        source_directory=f"addons/{name}",
        godot_version=godot_version or _latest_stable_godot_version,
    )
    _save(root_dir, details)


def load(project_root: Path | str) -> GAMProject:
    """Get the GAMProject information from a project root dir."""
    toml_file = Path(project_root).joinpath("gamproject.toml")
    if not toml_file.exists():
        raise FileNotFoundError()
    details = GAMProjectDetails(
        **{**parse(toml_file.read_text())["gamproject"], **{"path": project_root}}
    )
    return GAMProject(
        details=details, lock=_load_lock(project_root) or GAMLock(), path=project_root
    )


def _save(project_root: Path | str, gamproject: GAMProjectDetails) -> None:
    toml = dumps({"gamproject": gamproject.dict()})
    Path(project_root).joinpath("gamproject.toml").write_text(toml)


def _load_lock(project_root: Path) -> GAMLock | None:
    toml_file = Path(project_root).joinpath("gam.lock")
    if not toml_file.exists():
        return None
    return GAMLock(**parse(toml_file.read_text()).items())


def _save_lock(project_root: Path | str, lock: GAMLock) -> None:
    toml = dumps(lock.dict())
    Path(project_root).joinpath("gam.lock").write_text(toml)
