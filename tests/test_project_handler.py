"""Test GAM project IO and operations."""
import unittest
from pathlib import Path

from gamcore.gamconfig import GAMConfig
from gamcore.handlers.project import ProjectHandler


class ProjectHandlerTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        gam_config = Path().cwd() / "gam_config/config.toml"
        self.config = GAMConfig.get_instance(gam_config)
        self.config.cache_dir = Path().cwd() / "/gam_cache"
        super(ProjectHandlerTests, self).__init__(*args)

    def test_new(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        ProjectHandler.new(test_projects_dir, "test_new")
        self.assertTrue(test_projects_dir.joinpath("test_new/project.godot").exists())
        self.assertTrue(test_projects_dir.joinpath("test_new/gamproject.toml").exists())
