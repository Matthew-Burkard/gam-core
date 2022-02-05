"""Install a Godot asset."""
from gam_core import version
from gam_core.gamproject import GAMProjectDetails
from gam_core.project import GAMProject
from gam_core.requirement import Requirement
from gam_core.version import gather_dependencies


class AddHandler:
    """Class to manage adding a dependency to a project."""

    def __init__(self, project_config: GAMProject) -> None:
        self._gam_project = project_config
        self._requirements: list[Requirement] = []
        self._located_requirements: list[Requirement] = []

    def add(
        self, requirement_string: str, dev_dependency: bool = False
    ) -> GAMProjectDetails:
        """Add a dependency to a GAM project.

        :param requirement_string: String describing the dependency.
        :param dev_dependency: True if adding a dev dependency.
        :return: The details of the added dependency.
        """
        requirement = Requirement(requirement_string)
        self._requirements.extend(gather_dependencies([requirement]))
        # TODO Gather all dependencies.
        # TODO Install all requirements.
        return requirement.project_details

    def _all_requirements_located(self) -> bool:
        return all(self._is_requirement_met(r) for r in self._requirements)

    def _is_requirement_met(self, requirement: Requirement) -> bool:
        # Is this requirement already met?
        for installed in self._gam_project.installed:
            if requirement.project_details.name == installed.name:
                if version.matches(
                    requirement.requirement_string,
                    installed.version,
                ):
                    return True
        # Has a source for this requirement been located?
        for lr in self._located_requirements:
            if requirement.project_details.name == lr.project_details.name:
                if version.matches(
                    requirement.requirement_string,
                    lr.project_details.version,
                ):
                    return True
        return False
