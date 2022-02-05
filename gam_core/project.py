"""Manage IO to a GAM project config file."""
import re
from pathlib import Path

from tomlkit import dumps, parse

from gam_core.gamproject import GAMLock, GAMProjectDetails

_latest_stable_godot_version = "3.4.2"


class GAMProject:
    """Manage a GAM project."""

    def __init__(self, path: Path | str) -> None:
        self.details: GAMProjectDetails = []
        self.installed: list[GAMProjectDetails] = []
        self.lock: GAMLock | None = None
        self.path: Path = Path(path)
        self._load()

    @staticmethod
    def new(
        path: Path | str, name: str, godot_version: str | None = None
    ) -> "GAMProject":
        """Create a new "gamproject.toml" file."""
        if re.match(r"^(../|./|/)", path):
            name = re.search(r"(?<=/)([^/]+($|/$))", path).group(1)
            path = Path(path)
        else:
            name = path
            path = Path.cwd().joinpath(path)
        path.mkdir()
        details = GAMProjectDetails(
            name=name,
            version="0.1.0",
            source_directory=f"addons/{name}",
            godot_version=godot_version or _latest_stable_godot_version,
        )
        _save(path, details)
        return GAMProject(path)

    def _load(self) -> None:
        toml_file = self.path.joinpath("gamproject.toml")
        if not toml_file.exists():
            raise FileNotFoundError()
        details = GAMProjectDetails(
            **{**parse(toml_file.read_text())["gamproject"], **{"path": self.path}}
        )
        self.details = details
        self._load_lock()

    def _load_lock(self) -> None:
        toml_file = Path(self.path).joinpath("gam.lock")
        if not toml_file.exists():
            self.lock = GAMLock()
            return
        self.lock = GAMLock(**parse(toml_file.read_text()).items())


def _save(project_root: Path | str, gamproject: GAMProjectDetails) -> None:
    toml = dumps({"gamproject": gamproject.dict()})
    Path(project_root).joinpath("gamproject.toml").write_text(toml)


def _save_lock(project_root: Path | str, lock: GAMLock) -> None:
    toml = dumps(lock.dict())
    Path(project_root).joinpath("gam.lock").write_text(toml)
