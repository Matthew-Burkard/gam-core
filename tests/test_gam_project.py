"""GAM Core unit tests."""
import os
import shutil
import unittest
from pathlib import Path

from tomlkit import parse

from gam_core.gamconfig import GAMConfig
from gam_core.gamproject import GAMProject


class GAMTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        gam_config = Path().cwd() / "gam_config/config.toml"
        self.config = GAMConfig.get_instance(gam_config)
        self.config.cache_dir = Path().cwd() / "gam_cache"
        super(GAMTests, self).__init__(*args)

    def test_new(self) -> None:
        name = "test_new"
        root_dir = Path().cwd()
        project_dir = root_dir / name
        shutil.rmtree(project_dir, ignore_errors=True)
        new(project_dir.as_posix())
        os.chdir(root_dir)
        gamproject = GAMProject(
            **parse(project_dir.joinpath("gamproject.toml").read_text())["gamproject"]
        )
        self.assertEqual(gamproject.name, name)

    def test_build(self) -> None:
        project_a_root = Path.cwd().joinpath("test_projects/gd_project_a")
        self.gam.build(project_a_root)
        self.assertTrue(
            project_a_root.joinpath(f"dist/gd_project_a-0.1.0.tar.gz").is_file()
        )
        # TODO Unpack tarball and confirm contents are correct.

    def test_add(self) -> None:
        project_root = Path.cwd().joinpath("test_projects/gd_project_b")
        dependency_root = Path.cwd().joinpath("test_projects/gd_project_a")
        dependency_path = self.gam.build(dependency_root)
        self.gam.add(project_root, dependency_path.as_posix())
        addon_path = project_root.joinpath("addons/gd_project_a")
        self.assertTrue(addon_path.joinpath("gam_keep_me_a").is_file())
        self.assertTrue(addon_path.joinpath("kept/gam_kept_a").is_file())
