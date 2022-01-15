"""GAM Core unit tests."""
import os
import unittest
from pathlib import Path

from gam_core import _projectconfig


class ConfigTest(unittest.TestCase):
    def test_new(self) -> None:
        name = "test_config"
        root_dir = Path(os.getcwd()) / name
        _projectconfig.new(root_dir, name)
        gamproject = _projectconfig.load(root_dir)
        self.assertEqual(gamproject.name, name)


class BuildTest(unittest.TestCase):
    pass
