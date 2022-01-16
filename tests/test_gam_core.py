"""GAM Core unit tests."""
import os
import unittest
from pathlib import Path

from tomlkit import parse

from gam_core.gam import GAMCore
from gam_core.gamproject import GAMProject


class ConfigTest(unittest.TestCase):
    def __init__(self, *args) -> None:
        self.gam = GAMCore()
        super(ConfigTest, self).__init__(*args)

    def test_new(self) -> None:
        name = "test_config"
        root_dir = Path(os.getcwd()) / name
        self.gam.new((root_dir / name).as_posix())
        os.chdir(root_dir)
        gamproject = GAMProject(
            **parse(root_dir.joinpath("gamproject.toml").read_text())["gamproject"]
        )
        self.assertEqual(gamproject.name, name)


class BuildTest(unittest.TestCase):
    pass
