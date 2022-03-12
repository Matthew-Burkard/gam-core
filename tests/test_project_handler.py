"""Test GAM project IO and operations."""
import os
import shutil
import unittest
from pathlib import Path

from gamcore.gamconfig import GAMConfig
from gamcore.handlers.project import ProjectHandler
from gamcore.models import Package


class ProjectHandlerTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        gam_config = Path().cwd() / "gam_config/config.toml"
        self.config = GAMConfig.get_instance(gam_config)
        self.config.cache_dir = Path().cwd() / "gam_cache"
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

    def test_build(self) -> None:
        test_projects_dir = Path.cwd() / "test_projects"
        name = "test_build"
        shutil.rmtree(test_projects_dir.joinpath(name), ignore_errors=True)
        handler = ProjectHandler.new(test_projects_dir, name)
        test_projects_dir.joinpath(f"{name}/src/source_file").touch()
        test_projects_dir.joinpath(f"{name}/src/sub_dir").mkdir()
        test_projects_dir.joinpath(f"{name}/src/sub_dir/file").touch()
        handler.build()
        self.assertTrue(
            test_projects_dir.joinpath(f"{name}/dist/{name}-0.1.0.tar.gz").exists()
        )
        self.assertTrue(
            test_projects_dir.joinpath(f"{name}/dist/{name}-0.1.0/source_file").exists()
        )
        self.assertTrue(
            test_projects_dir.joinpath(
                f"{name}/dist/{name}-0.1.0/sub_dir/file"
            ).exists()
        )

    def test_lock_io(self) -> None:
        name = "test_lock_io"
        test_projects_dir = Path.cwd() / "test_projects"
        shutil.rmtree(test_projects_dir.joinpath(name), ignore_errors=True)
        handler = ProjectHandler.new(test_projects_dir, name)
        packages = [
            Package(dependencies={"coffee": "^1.0.0", "caramel": "0.1.0"}),
            Package(dependencies={"coffee": "^1.1.0", "donut": "2.1.0"}),
        ]
        # This isn't a straightforward setter/getter.
        handler.lock_packages = packages
        self.assertEqual(packages, handler.lock_packages)
