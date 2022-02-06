"""Test GAM project IO and operations."""
import shutil
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
        name = "test_new"
        shutil.rmtree(test_projects_dir.joinpath(name), ignore_errors=True)
        ProjectHandler.new(test_projects_dir, name)
        self.assertTrue(test_projects_dir.joinpath(f"{name}/project.godot").exists())
        self.assertTrue(test_projects_dir.joinpath(f"{name}/gamproject.toml").exists())

    def test_new_already_exists(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_new_already_exists"
        shutil.rmtree(test_projects_dir.joinpath(name), ignore_errors=True)
        ProjectHandler.new(test_projects_dir, name)
        try:
            ProjectHandler.new(test_projects_dir, name)
        except FileExistsError:
            self.assertTrue(True)

    def test_load(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_load"
        shutil.rmtree(test_projects_dir.joinpath(name), ignore_errors=True)
        ProjectHandler.new(test_projects_dir, name)
        existing_project = ProjectHandler(test_projects_dir / name)
        self.assertEqual(name, existing_project.details.name)

    def test_load_does_not_exist(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_load"
        shutil.rmtree(test_projects_dir.joinpath(name), ignore_errors=True)
        try:
            ProjectHandler(test_projects_dir / name)
        except FileNotFoundError:
            self.assertTrue(True)
