"""Check version compatability."""
from gam_core.requirement import Requirement


def gather_dependencies(requirements: list[Requirement]) -> list[Requirement]:
    """Gather all dependencies for the given requirements."""
    for requirement in requirements:
        for dependency in requirement.project_details.dependencies:
            if any(matches(dependency, r.requirement_string) for r in requirements):
                continue
            requirements.append(Requirement(dependency))
            return gather_dependencies(requirements)
    return requirements


def matches(version: str, requirement: str) -> bool:
    """Check if a version matches a version requirement."""
    pass  # TODO
