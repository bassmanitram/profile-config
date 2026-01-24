#!/usr/bin/env python3
"""
Example demonstrating the automatic creation of the "default" profile.

This example shows how the "default" profile works with and without
explicit definition in the configuration file.
"""

import os
import tempfile
from pathlib import Path

from profile_config import ProfileConfigResolver


def demo_auto_created_default():
    """Demonstrate automatic creation of default profile."""
    print("=" * 70)
    print("Example 1: Auto-created 'default' profile")
    print("=" * 70)

    config_content = """
# Configuration without explicit "default" profile
defaults:
  host: localhost
  port: 5432
  timeout: 30
  debug: false

profiles:
  development:
    debug: true
    port: 3000
    log_level: DEBUG

  production:
    host: prod-db.example.com
    timeout: 60
    log_level: ERROR
"""

    print("\nConfiguration file:")
    print("-" * 70)
    print(config_content)
    print("-" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save current directory
        original_dir = os.getcwd()

        try:
            # Create config file
            os.chdir(tmpdir)
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(config_content)

            # Resolve default profile (auto-created)
            resolver = ProfileConfigResolver(
                "myapp", profile="default", search_home=False
            )
            config = resolver.resolve()

            print("\nResult with profile='default' (auto-created):")
            print("-" * 70)
            for key, value in sorted(config.items()):
                print(f"  {key}: {value}")
            print()

            # Compare with development profile
            resolver_dev = ProfileConfigResolver(
                "myapp", profile="development", search_home=False
            )
            config_dev = resolver_dev.resolve()

            print("\nCompare with profile='development':")
            print("-" * 70)
            for key, value in sorted(config_dev.items()):
                print(f"  {key}: {value}")
            print()

        finally:
            os.chdir(original_dir)


def demo_explicit_default():
    """Demonstrate explicit default profile."""
    print("=" * 70)
    print("Example 2: Explicit 'default' profile")
    print("=" * 70)

    config_content = """
# Configuration with explicit "default" profile
defaults:
  host: localhost
  port: 5432
  timeout: 30
  debug: false

profiles:
  default:
    # Override some defaults for the default profile
    timeout: 45
    custom_setting: true
    environment: base

  development:
    inherits: default
    debug: true
    port: 3000
    environment: dev
"""

    print("\nConfiguration file:")
    print("-" * 70)
    print(config_content)
    print("-" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()

        try:
            os.chdir(tmpdir)
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(config_content)

            # Resolve explicit default profile
            resolver = ProfileConfigResolver(
                "myapp", profile="default", search_home=False
            )
            config = resolver.resolve()

            print("\nResult with profile='default' (explicit definition):")
            print("-" * 70)
            for key, value in sorted(config.items()):
                print(f"  {key}: {value}")
            print()

            # Show development inheriting from default
            resolver_dev = ProfileConfigResolver(
                "myapp", profile="development", search_home=False
            )
            config_dev = resolver_dev.resolve()

            print("\nResult with profile='development' (inherits from default):")
            print("-" * 70)
            for key, value in sorted(config_dev.items()):
                print(f"  {key}: {value}")
            print()

        finally:
            os.chdir(original_dir)


def demo_environment_fallback():
    """Demonstrate using default as environment fallback."""
    print("=" * 70)
    print("Example 3: Using 'default' as environment fallback")
    print("=" * 70)

    config_content = """
defaults:
  host: localhost
  port: 5432
  log_level: INFO

profiles:
  development:
    debug: true
    log_level: DEBUG

  production:
    host: prod-db.example.com
    log_level: WARNING
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()

        try:
            os.chdir(tmpdir)
            config_dir = Path(tmpdir) / "myapp"
            config_dir.mkdir()
            config_file = config_dir / "config.yaml"
            config_file.write_text(config_content)

            # Simulate different environment variables
            test_cases = [
                ("development", "Development environment"),
                ("production", "Production environment"),
                (None, "No environment specified (falls back to default)"),
            ]

            for env_value, description in test_cases:
                print(f"\n{description}:")
                print("-" * 70)

                # Simulate environment variable
                env = env_value if env_value else "default"

                resolver = ProfileConfigResolver(
                    "myapp", profile=env, search_home=False
                )
                config = resolver.resolve()

                print(f"Profile used: {env}")
                for key, value in sorted(config.items()):
                    print(f"  {key}: {value}")
            print()

        finally:
            os.chdir(original_dir)


def main():
    """Run all examples."""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  Default Profile Auto-Creation Examples".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print()

    demo_auto_created_default()
    demo_explicit_default()
    demo_environment_fallback()

    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print("""
The 'default' profile provides flexible configuration:

1. Auto-Creation: When no 'default' profile exists, it returns only
   the defaults section values.

2. Explicit Definition: You can define a 'default' profile to customize
   the baseline configuration.

3. Environment Fallback: Use 'default' as a fallback when no specific
   environment is specified.

This makes it easy to:
- Get base configuration without profile-specific overrides
- Test applications with minimal configuration
- Provide sensible defaults for local development
""")


if __name__ == "__main__":
    main()
