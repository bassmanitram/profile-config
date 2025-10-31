"""
Tests for the main ProfileConfigResolver.
"""

import os
import tempfile
from pathlib import Path

import pytest

from profile_config import ProfileConfigResolver
from profile_config.exceptions import ConfigNotFoundError, ProfileNotFoundError


class TestProfileConfigResolver:
    """Test main profile configuration resolver."""

    def test_init_default_values(self):
        """Test initialization with default values."""
        resolver = ProfileConfigResolver("myapp")

        assert resolver.config_name == "myapp"
        assert resolver.profile == "default"
        assert resolver.override_list == []
        assert resolver.enable_interpolation is True

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        overrides = {"key": "override_value"}
        resolver = ProfileConfigResolver(
            "testapp",
            profile="dev",
            overrides=overrides,
            extensions=["yaml"],
            search_home=False,
            enable_interpolation=False,
        )

        assert resolver.config_name == "testapp"
        assert resolver.profile == "dev"
        assert resolver.override_list == [overrides]
        assert resolver.enable_interpolation is False

    def test_resolve_simple_config(self):
        """Test resolving a simple configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                """
defaults:
  database: sqlite:///default.db
  debug: false

profiles:
  dev:
    debug: true
    database: sqlite:///dev.db
"""
            )

            resolver = ProfileConfigResolver("myapp", profile="dev", search_home=False)
            result = resolver.resolve()

            expected = {"database": "sqlite:///dev.db", "debug": True}
            assert result == expected

    def test_resolve_with_inheritance(self):
        """Test resolving configuration with profile inheritance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                """
defaults:
  timeout: 30

profiles:
  base:
    database: sqlite:///base.db
    debug: false

  dev:
    inherits: base
    debug: true
    port: 3000
"""
            )

            resolver = ProfileConfigResolver("myapp", profile="dev", search_home=False)
            result = resolver.resolve()

            expected = {
                "timeout": 30,  # From defaults
                "database": "sqlite:///base.db",  # From base profile
                "debug": True,  # Dev overrides base
                "port": 3000,  # Dev-specific
            }
            assert result == expected

    def test_resolve_with_overrides(self):
        """Test resolving configuration with overrides."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                """
defaults:
  database: sqlite:///default.db
  port: 8000

profiles:
  dev:
    debug: true
"""
            )

            overrides = {
                "database": "postgresql://localhost/override",
                "new_key": "override_value",
            }

            resolver = ProfileConfigResolver(
                "myapp", profile="dev", overrides=overrides, search_home=False
            )
            result = resolver.resolve()

            expected = {
                "database": "postgresql://localhost/override",  # Override wins
                "port": 8000,  # From defaults
                "debug": True,  # From profile
                "new_key": "override_value",  # From overrides
            }
            assert result == expected

    def test_resolve_multiple_config_files(self):
        """Test resolving with multiple configuration files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create base config in parent directory
            parent_config_dir = Path(tmpdir) / "myapp"
            parent_config_dir.mkdir()
            parent_config = parent_config_dir / "config.yaml"
            parent_config.write_text(
                """
defaults:
  database: sqlite:///parent.db
  timeout: 30

profiles:
  dev:
    debug: false
"""
            )

            # Create more specific config in subdirectory
            sub_dir = Path(tmpdir) / "project"
            sub_dir.mkdir()
            sub_config_dir = sub_dir / "myapp"
            sub_config_dir.mkdir()
            sub_config = sub_config_dir / "config.yaml"
            sub_config.write_text(
                """
defaults:
  database: sqlite:///project.db

profiles:
  dev:
    debug: true
    port: 3000
"""
            )

            # Change to subdirectory
            os.chdir(sub_dir)

            resolver = ProfileConfigResolver("myapp", profile="dev", search_home=False)
            result = resolver.resolve()

            expected = {
                "database": "sqlite:///project.db",  # More specific config wins
                "timeout": 30,  # From parent config
                "debug": True,  # More specific config wins
                "port": 3000,  # From more specific config
            }
            assert result == expected

    def test_resolve_with_interpolation(self):
        """Test resolving configuration with variable interpolation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file with interpolation
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                """
defaults:
  base_path: /app
  data_path: ${base_path}/data
  log_path: ${base_path}/logs

profiles:
  dev:
    base_path: /dev/app
"""
            )

            resolver = ProfileConfigResolver("myapp", profile="dev", search_home=False)
            result = resolver.resolve()

            expected = {
                "base_path": "/dev/app",
                "data_path": "/dev/app/data",  # Interpolated
                "log_path": "/dev/app/logs",  # Interpolated
            }
            assert result == expected

    def test_resolve_interpolation_disabled(self):
        """Test resolving configuration with interpolation disabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file with interpolation
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                """
defaults:
  base_path: /app
  data_path: ${base_path}/data
"""
            )

            resolver = ProfileConfigResolver(
                "myapp", search_home=False, enable_interpolation=False
            )
            result = resolver.resolve()

            expected = {
                "base_path": "/app",
                "data_path": "${base_path}/data",  # Not interpolated
            }
            assert result == expected

    def test_resolve_nonexistent_profile(self):
        """Test resolving a nonexistent profile."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                """
profiles:
  dev:
    debug: true
"""
            )

            resolver = ProfileConfigResolver(
                "myapp", profile="nonexistent", search_home=False
            )

            with pytest.raises(ProfileNotFoundError):
                resolver.resolve()

    def test_resolve_no_config_files(self):
        """Test resolving when no config files exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            resolver = ProfileConfigResolver("nonexistent", search_home=False)

            with pytest.raises(ConfigNotFoundError):
                resolver.resolve()

    def test_list_profiles(self):
        """Test listing available profiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(
                """
profiles:
  dev:
    debug: true
  staging:
    debug: false
  prod:
    debug: false
"""
            )

            resolver = ProfileConfigResolver("myapp", search_home=False)
            profiles = resolver.list_profiles()

            assert set(profiles) == {"dev", "staging", "prod"}

    def test_list_profiles_no_config(self):
        """Test listing profiles when no config files exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            resolver = ProfileConfigResolver("nonexistent", search_home=False)
            profiles = resolver.list_profiles()

            assert profiles == []

    def test_get_config_files(self):
        """Test getting discovered configuration files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            # Create config file
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text("test: value")

            resolver = ProfileConfigResolver("myapp", search_home=False)
            files = resolver.get_config_files()

            assert len(files) == 1
            assert files[0] == config_file

    def test_get_config_files_no_config(self):
        """Test getting config files when none exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)

            resolver = ProfileConfigResolver("nonexistent", search_home=False)
            files = resolver.get_config_files()

            assert files == []
