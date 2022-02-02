"""Unit tests around requirements."""
import unittest
from pathlib import Path

from gam_core.gamconfig import GAMConfig
from gam_core.gamproject import GAMProjectDetails
from gam_core.requirement import Requirement, RequirementSourceType


class RequirementTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        gam_config = Path().cwd() / "gam_config/config.toml"
        self.config = GAMConfig.get_instance(gam_config)
        self.config.cache_dir = Path().cwd() / "gam_cache"
        super(RequirementTests, self).__init__(*args)

    def test_filepath_requirement_type(self) -> None:
        filepath_req = Path.cwd() / "test_projects/gd_project_a-0.1.0.tar.gz"
        requirement = Requirement(filepath_req.as_posix())
        self.assertEqual(RequirementSourceType.FILE, requirement.source)

    def test_filepath_project_details(self) -> None:
        filepath_req = Path.cwd() / "test_projects/gd_project_a-0.1.0.tar.gz"
        requirement = Requirement(filepath_req.as_posix())
        details = GAMProjectDetails(
            name="gd_project_a",
            version="0.1.0",
            godot_version="3.4.2",
            source_directory="src",
            packages=["./gam_keep_me_a", "./kept/"]
        )
        self.assertEqual(details, requirement.project_details)
