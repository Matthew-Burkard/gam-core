"""Test GAMConfig management."""
import shutil
import unittest
from pathlib import Path

import tomlkit

from gamcore.gamconfig import GAMConfig


class GAMConfigTests(unittest.TestCase):
    def __init__(self, *args) -> None:
        cache_dir = Path().cwd() / "gam_cache"
        shutil.rmtree(cache_dir, ignore_errors=True)
        super(GAMConfigTests, self).__init__(*args)

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
        GAMConfig.__instance__ = None
        gam_config = Path().cwd() / "gam_cache/new_config/a/config.toml"
        # Make it twice to confirm it's no problem if it already exists.
        config = GAMConfig.get_instance(gam_config)
        config.save()
        GAMConfig.__instance__ = None
        config = GAMConfig.get_instance(gam_config)
        config.save()
        # Make it once after confirming it doesn't exist.
        GAMConfig.__instance__ = None
        shutil.rmtree(Path().cwd() / "gam_cache/new_config/", ignore_errors=True)
        config = GAMConfig.get_instance(gam_config)
        config.save()
        self.assertTrue(gam_config.is_file())

    def test_tmp_dir(self) -> None:
        GAMConfig.__instance__ = None
        gam_config = Path().cwd() / "gam_config/config.toml"
        config = GAMConfig.get_instance(gam_config)
        cache_dir = Path().cwd() / "gam_cache"
        config.cache_dir = cache_dir
        tmp_dir = cache_dir.joinpath("tmp")
        self.assertEqual(tmp_dir.resolve(), config.tmp_dir.resolve())
        try:
            config.tmp_dir = tmp_dir
        except AssertionError:
            self.assertTrue(True)

    def test_new_cache_dir(self) -> None:
        GAMConfig.__instance__ = None
        gam_config = Path().cwd() / "gam_cache/new_config/a/config.toml"
        gam_cache = Path().cwd() / "gam_cache/new_config/a/cache"
        config = GAMConfig.get_instance(gam_config)
        config.cache_dir = gam_cache
        config.save()
        print(gam_config.read_text())
        self.assertEqual(
            gam_cache.resolve().as_posix(),
            tomlkit.loads(gam_config.read_text())["gam"]["cache_dir"],
        )

    def test_singleton(self) -> None:
        GAMConfig.__instance__ = None
        gam_config = Path().cwd() / "gam_config/config.toml"
        GAMConfig.get_instance(gam_config)
        try:
            GAMConfig(gam_config)
        except AssertionError:
            self.assertTrue(True)
