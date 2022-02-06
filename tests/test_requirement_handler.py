"""Unit test_projects around requirements."""
import shutil
import unittest
from pathlib import Path

from gamcore.gamconfig import GAMConfig
from gamcore.handlers.project import ProjectHandler
from gamcore.handlers.requirement import RequirementHandler, RequirementSourceType
from gamcore.models import GAMProject


class RequirementHandlerTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        gam_config = Path().cwd() / "gam_config/config.toml"
        self.config = GAMConfig.get_instance(gam_config)
        self.config.cache_dir = Path().cwd() / "gam_cache"
        super(RequirementHandlerTests, self).__init__(*args)

    def test_filepath_requirement_type(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_filepath_req"
        shutil.rmtree(test_projects_dir / name, ignore_errors=True)
        new_project = ProjectHandler.new(test_projects_dir, name)
        filepath_req = new_project.build()
        requirement = RequirementHandler(filepath_req.as_posix())
        self.assertEqual(RequirementSourceType.FILE, requirement.source)

    def test_filepath_project_details(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_filepath_details"
        shutil.rmtree(test_projects_dir / name, ignore_errors=True)
        new_project = ProjectHandler.new(test_projects_dir, name)
        filepath_req = new_project.build()
        requirement = RequirementHandler(filepath_req.as_posix())
        details = GAMProject(
            name=name,
            version="0.1.0",
            godot_version=">=4.0",
            source_directory="src",
            packages=["**/*"],
        )
        self.assertEqual(details, requirement.project_details)
