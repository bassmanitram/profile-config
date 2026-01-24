"""
Example demonstrating environment variable injection feature.

This example shows how to use the env_vars feature to automatically
set environment variables from your configuration.
"""

import os
import tempfile
from pathlib import Path

from profile_config import ProfileConfigResolver


def main():
    """Demonstrate environment variable injection."""
    # Create a temporary directory for our example
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create example configuration
        config_dir = Path(tmpdir) / "myapp"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text("""
defaults:
  app_name: myapp
  database:
    host: localhost
    port: 5432
  api:
    base_url: http://localhost:8000
  env_vars:
    APP_NAME: "${app_name}"
    DATABASE_URL: "postgresql://${database.host}:${database.port}/mydb"
    API_BASE_URL: "${api.base_url}"
    LOG_LEVEL: "INFO"

profiles:
  development:
    database:
      host: dev-db.local
    env_vars:
      LOG_LEVEL: "DEBUG"
      ENVIRONMENT: "development"

  production:
    database:
      host: prod-db.example.com
    api:
      base_url: https://api.example.com
    env_vars:
      LOG_LEVEL: "WARNING"
      ENVIRONMENT: "production"
""")

        # Change to tmpdir so the resolver can find our config
        original_cwd = os.getcwd()
        os.chdir(tmpdir)

        try:
            print("=" * 60)
            print("Environment Variable Injection Example")
            print("=" * 60)

            # Example 1: Default profile
            print("\n1. Using default profile:")
            print("-" * 60)
            resolver = ProfileConfigResolver("myapp", search_home=False)
            config = resolver.resolve()

            print("\nEnvironment variables set:")
            for key in ["APP_NAME", "DATABASE_URL", "API_BASE_URL", "LOG_LEVEL"]:
                print(f"  {key} = {os.environ.get(key)}")

            env_info = resolver.get_environment_info()
            print(f"\nEnvironment info:")
            print(f"  Applied: {len(env_info['applied'])} variables")
            print(f"  Skipped: {len(env_info['skipped'])} variables")

            # Clean up env vars
            for key in ["APP_NAME", "DATABASE_URL", "API_BASE_URL", "LOG_LEVEL"]:
                os.environ.pop(key, None)

            # Example 2: Development profile
            print("\n\n2. Using development profile:")
            print("-" * 60)
            resolver = ProfileConfigResolver(
                "myapp", profile="development", search_home=False
            )
            config = resolver.resolve()

            print("\nEnvironment variables set:")
            for key in [
                "APP_NAME",
                "DATABASE_URL",
                "API_BASE_URL",
                "LOG_LEVEL",
                "ENVIRONMENT",
            ]:
                print(f"  {key} = {os.environ.get(key)}")

            # Clean up env vars
            for key in [
                "APP_NAME",
                "DATABASE_URL",
                "API_BASE_URL",
                "LOG_LEVEL",
                "ENVIRONMENT",
            ]:
                os.environ.pop(key, None)

            # Example 3: Production profile
            print("\n\n3. Using production profile:")
            print("-" * 60)
            resolver = ProfileConfigResolver(
                "myapp", profile="production", search_home=False
            )
            config = resolver.resolve()

            print("\nEnvironment variables set:")
            for key in [
                "APP_NAME",
                "DATABASE_URL",
                "API_BASE_URL",
                "LOG_LEVEL",
                "ENVIRONMENT",
            ]:
                print(f"  {key} = {os.environ.get(key)}")

            # Clean up env vars
            for key in [
                "APP_NAME",
                "DATABASE_URL",
                "API_BASE_URL",
                "LOG_LEVEL",
                "ENVIRONMENT",
            ]:
                os.environ.pop(key, None)

            # Example 4: Respecting existing environment variables
            print("\n\n4. Respecting existing environment variables:")
            print("-" * 60)
            os.environ["LOG_LEVEL"] = "ERROR"  # Set existing var
            print(f"Existing LOG_LEVEL: {os.environ['LOG_LEVEL']}")

            resolver = ProfileConfigResolver(
                "myapp",
                profile="development",
                search_home=False,
                override_environment=False,  # Don't override existing vars
            )
            config = resolver.resolve()

            print(f"After resolve, LOG_LEVEL: {os.environ['LOG_LEVEL']}")
            print("  (Not overridden because override_environment=False)")

            env_info = resolver.get_environment_info()
            print(f"\nSkipped variables (already exist):")
            for key, value in env_info["skipped"].items():
                print(f"  {key}: config wanted '{value}', kept existing value")

            # Clean up
            for key in [
                "APP_NAME",
                "DATABASE_URL",
                "API_BASE_URL",
                "LOG_LEVEL",
                "ENVIRONMENT",
            ]:
                os.environ.pop(key, None)

            # Example 5: Overriding existing environment variables
            print("\n\n5. Overriding existing environment variables:")
            print("-" * 60)
            os.environ["LOG_LEVEL"] = "ERROR"  # Set existing var
            print(f"Existing LOG_LEVEL: {os.environ['LOG_LEVEL']}")

            resolver = ProfileConfigResolver(
                "myapp",
                profile="development",
                search_home=False,
                override_environment=True,  # Override existing vars
            )
            config = resolver.resolve()

            print(f"After resolve, LOG_LEVEL: {os.environ['LOG_LEVEL']}")
            print("  (Overridden because override_environment=True)")

            # Clean up
            for key in [
                "APP_NAME",
                "DATABASE_URL",
                "API_BASE_URL",
                "LOG_LEVEL",
                "ENVIRONMENT",
            ]:
                os.environ.pop(key, None)

            print("\n" + "=" * 60)
            print("Note: env_vars section is removed from returned config")
            print(f"Config keys: {list(config.keys())}")
            print("=" * 60)

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    main()
