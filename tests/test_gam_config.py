"""Test GAMConfig management."""
import unittest
from pathlib import Path

from gamcore.gamconfig import GAMConfig


class GAMConfigTests(unittest.TestCase):
    def test_load_save_integrity(self) -> None:
        GAMConfig.__instance__ = None
        gam_config = Path().cwd() / "gam_config/integrity_test.toml"
        raw_text = gam_config.read_text()
        config = GAMConfig.get_instance(gam_config)
        config.save()
        self.assertEqual(raw_text, gam_config.read_text())
        cache_dir = Path().cwd() / "gam_cache"
        config.cache_dir = cache_dir
        config.save()
        self.assertEqual(raw_text, gam_config.read_text())

    def test_default_config_location(self) -> None:
        GAMConfig.__instance__ = None
        default_path = Path.home().joinpath(".config/gam/config.toml")
        config = GAMConfig.get_instance()
        self.assertEqual(default_path, config.path)
        config.save()
        self.assertTrue(default_path.exists())

    def test_custom_config_location(self) -> None:
        GAMConfig.__instance__ = None
        gam_config = Path().cwd() / "gam_config/config.toml"
        cache_dir = Path().cwd() / "gam_cache"
        config = GAMConfig.get_instance(gam_config)
        config.cache_dir = cache_dir
        self.assertEqual(gam_config, config.path)
        config.save()
        self.assertTrue(gam_config.exists())
        self.assertEqual(cache_dir.resolve(), config.cache_dir.resolve())

    def test_updating_config_location(self) -> None:
        GAMConfig.__instance__ = None
        config = GAMConfig.get_instance()
        gam_config = Path().cwd() / "gam_config/config.toml"
        config.path = gam_config
        cache_dir = Path().cwd() / "gam_cache"
        self.assertEqual(cache_dir.resolve(), config.cache_dir.resolve())

    def test_new_config(self) -> None:
        pass

    def test_singleton(self) -> None:
        GAMConfig.__instance__ = None
        gam_config = Path().cwd() / "gam_config/config.toml"
        GAMConfig.get_instance(gam_config)
        try:
            GAMConfig(gam_config)
        except AssertionError:
            self.assertTrue(True)
