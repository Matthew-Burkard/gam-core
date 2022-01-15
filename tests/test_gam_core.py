"""GAM Core unit tests."""
import os
import unittest
from pathlib import Path

from gam_core import projectconfig


class ConfigTest(unittest.TestCase):
    def test_new(self) -> None:
        name = "test_config"
        root_dir = Path(os.getcwd()) / name
        projectconfig.new(root_dir, name)
        gamproject = projectconfig.load(root_dir)
        self.assertEqual(gamproject.name, name)


class BuildTest(unittest.TestCase):
    pass
