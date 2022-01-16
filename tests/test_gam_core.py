"""GAM Core unit tests."""
import os
import unittest
from pathlib import Path

from tomlkit import parse

from gam_core.gam import GAMCore
from gam_core.gamproject import GAMProject


class GAMTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        gam_config = Path().cwd() / "gam_config"
        gam_cache = Path().cwd() / "gam_cache"
        self.gam = GAMCore(config_dir=gam_config, cache_dir=gam_cache)
        super(GAMTests, self).__init__(*args)

    def test_new(self) -> None:
        name = "test_config"
        root_dir = Path().cwd() / name
        self.gam.new((root_dir / name).as_posix())
        os.chdir(root_dir)
        gamproject = GAMProject(
            **parse(root_dir.joinpath("gamproject.toml").read_text())["gamproject"]
        )
        self.assertEqual(gamproject.name, name)

    def test_build(self) -> None:
        pass
