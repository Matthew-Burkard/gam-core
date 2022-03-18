"""Add a requirement to a project."""
from pathlib import Path

from gamcore._util import get_installed_packages
from gamcore.handlers.install import InstallHandler
from gamcore.handlers.requirement import RequirementHandler


class AddHandler:
    """Handle adding a requirement."""

    def __init__(
        self,
        project_path: str | Path,
        requirement: RequirementHandler,
    ) -> None:
        """Init a handler to add a requirement.

        :param project_path: Path to project adding a requirement.
        :param requirement: The requirement being added.
        """
        self._project_path = project_path
        self._requirement = requirement
        # All dependencies.
        self._dependencies: dict[str, str] = {}
        # Dependencies that are already installed.
        self._installed_dependencies: dict[str, str] = {}
        # Dependencies that need to be installed.
        self._unmet_requirements: list[RequirementHandler] = [requirement]

    def execute(self) -> None:
        """Add the package."""
        self._gather_requirements()
        self._project_path.joinpath("addons").mkdir(exist_ok=True)
        for req in self._unmet_requirements:
            InstallHandler(self._project_path, req).execute()
        InstallHandler(self._project_path, self._requirement).execute()

    def _gather_requirements(self) -> None:
        self._get_dependencies(self._requirement)
        self._installed_dependencies = {
            it.name: it.version
            for it in get_installed_packages(self._project_path)
            if it.name in self._dependencies
        }
        unmet_dependencies = {
            dep: version
            for dep, version in self._dependencies.items()
            if not (installed_dep_ver := self._installed_dependencies.get(dep))
            or not self._is_compatible(installed_dep_ver, version)
        }
        for dep, version in unmet_dependencies.items():
            self._unmet_requirements.append(RequirementHandler(f"{dep}@{version}"))

    def _get_dependencies(self, requirement: RequirementHandler) -> None:
        for name, rule in requirement.project_details.dependencies.items():
            if name in self._dependencies and rule != self._dependencies[name]:
                self._dependencies[name] = self._get_compatible_rule(
                    rule, self._dependencies[name]
                )
                self._get_dependencies(RequirementHandler(f"{name}@{rule}"))
            elif name not in self._dependencies:
                self._dependencies[name] = rule
                self._get_dependencies(RequirementHandler(f"{name}@{rule}"))

    def _get_installed_dependencies(self) -> dict[str, str]:
        """Get all dependencies already installed in this project."""

    def _get_compatible_rule(self, version_rule: str, other: str) -> str:
        """Get a new version rule that is compatible existing rules."""

    @staticmethod
    def _is_compatible(version_rule: str, other: str) -> bool:
        # TODO
        return True
