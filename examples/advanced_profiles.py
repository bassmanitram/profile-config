#!/usr/bin/env python3
"""
Advanced profile usage example for profile-config.

This example demonstrates complex profile inheritance patterns and
advanced configuration management scenarios.
"""

from pathlib import Path

from profile_config import ProfileConfigResolver
from profile_config.exceptions import CircularInheritanceError, ProfileNotFoundError


def create_complex_config():
    """Create a complex configuration with multi-level inheritance."""
    config_content = """
# Global defaults
defaults:
  timeout: 30
  retries: 3
  log_level: INFO

# Profile hierarchy
profiles:
  # Base configuration
  base:
    database:
      driver: postgresql
      host: localhost
      port: 5432
    cache:
      enabled: true
      ttl: 3600
    features:
      feature_a: true
      feature_b: false

  # Development base
  dev_base:
    inherits: base
    database:
      host: dev-db.local
      name: myapp_dev
    log_level: DEBUG
    features:
      feature_b: true

  # Local development
  local:
    inherits: dev_base
    database:
      driver: sqlite
      path: ./local.db
    cache:
      enabled: false

  # Remote development
  remote_dev:
    inherits: dev_base
    database:
      host: remote-dev.example.com
      ssl: true
    monitoring:
      enabled: true

  # Staging base
  staging_base:
    inherits: base
    database:
      host: staging-db.example.com
      name: myapp_staging
    cache:
      ttl: 1800

  # Staging
  staging:
    inherits: staging_base
    monitoring:
      enabled: true
      alerts: true

  # Production base
  prod_base:
    inherits: base
    database:
      host: prod-db.example.com
      name: myapp_prod
      pool_size: 20
    cache:
      ttl: 7200
    timeout: 60
    retries: 5

  # Production
  production:
    inherits: prod_base
    log_level: WARNING
    monitoring:
      enabled: true
      alerts: true
      metrics: true
    features:
      feature_a: true
      feature_b: true
      feature_c: true
"""

    # Create config directory and file
    config_dir = Path("complex-app")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text(config_content)

    print(f"Created complex config at: {config_file.absolute()}")
    return config_file


def demonstrate_inheritance_chain():
    """Demonstrate complex inheritance chains."""
    print("=== Complex Inheritance Chain Example ===\n")

    config_file = create_complex_config()

    try:
        # Show inheritance chain for production
        print("1. Production profile inheritance chain:")
        print("   production -> prod_base -> base -> defaults")
        print()

        resolver = ProfileConfigResolver("complex-app", profile="production")
        prod_config = resolver.resolve()

        print("   Resolved production configuration:")
        for key, value in sorted(prod_config.items()):
            if isinstance(value, dict):
                print(f"   {key}:")
                for sub_key, sub_value in sorted(value.items()):
                    print(f"     {sub_key}: {sub_value}")
            else:
                print(f"   {key}: {value}")
        print()

        # Compare with local development
        print("2. Local development profile inheritance chain:")
        print("   local -> dev_base -> base -> defaults")
        print()

        resolver = ProfileConfigResolver("complex-app", profile="local")
        local_config = resolver.resolve()

        print("   Resolved local configuration:")
        for key, value in sorted(local_config.items()):
            if isinstance(value, dict):
                print(f"   {key}:")
                for sub_key, sub_value in sorted(value.items()):
                    print(f"     {sub_key}: {sub_value}")
            else:
                print(f"   {key}: {value}")
        print()

    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_profile_comparison():
    """Demonstrate comparing different profiles."""
    print("=== Profile Comparison Example ===\n")

    config_file = create_complex_config()

    try:
        profiles_to_compare = ["local", "staging", "production"]
        configs = {}

        # Resolve all profiles
        for profile in profiles_to_compare:
            resolver = ProfileConfigResolver("complex-app", profile=profile)
            configs[profile] = resolver.resolve()

        # Compare specific settings
        print("Database configuration comparison:")
        print(f"{'Setting':<15} {'Local':<20} {'Staging':<20} {'Production':<20}")
        print("-" * 80)

        db_settings = ["driver", "host", "name", "port", "pool_size"]
        for setting in db_settings:
            values = []
            for profile in profiles_to_compare:
                db_config = configs[profile].get("database", {})
                value = db_config.get(setting, "N/A")
                values.append(str(value)[:19])  # Truncate for display

            print(f"{setting:<15} {values[0]:<20} {values[1]:<20} {values[2]:<20}")
        print()

        # Compare feature flags
        print("Feature flags comparison:")
        print(f"{'Feature':<15} {'Local':<10} {'Staging':<10} {'Production':<10}")
        print("-" * 50)

        all_features = set()
        for config in configs.values():
            features = config.get("features", {})
            all_features.update(features.keys())

        for feature in sorted(all_features):
            values = []
            for profile in profiles_to_compare:
                features = configs[profile].get("features", {})
                value = features.get(feature, False)
                values.append(str(value))

            print(f"{feature:<15} {values[0]:<10} {values[1]:<10} {values[2]:<10}")
        print()

    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_error_handling():
    """Demonstrate error handling scenarios."""
    print("=== Error Handling Examples ===\n")

    # Example 1: Circular inheritance
    print("1. Circular inheritance detection:")
    circular_config = """
profiles:
  a:
    inherits: b
    value: a_value
  b:
    inherits: c
    value: b_value
  c:
    inherits: a
    value: c_value
"""

    config_dir = Path("error-demo")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text(circular_config)

    try:
        resolver = ProfileConfigResolver("error-demo", profile="a")
        try:
            resolver.resolve()
        except CircularInheritanceError as e:
            print(f"   Caught CircularInheritanceError: {e}")
        print()

        # Example 2: Nonexistent profile
        print("2. Nonexistent profile handling:")
        try:
            resolver = ProfileConfigResolver("error-demo", profile="nonexistent")
            resolver.resolve()
        except ProfileNotFoundError as e:
            print(f"   Caught ProfileNotFoundError: {e}")
        print()

        # Example 3: Profile listing for debugging
        print("3. Available profiles for debugging:")
        resolver = ProfileConfigResolver("error-demo")
        profiles = resolver.list_profiles()
        print(f"   Available profiles: {profiles}")
        print()

    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_custom_inheritance_key():
    """Demonstrate using custom inheritance key."""
    print("=== Custom Inheritance Key Example ===\n")

    config_content = """
profiles:
  base:
    database: sqlite:///base.db
    debug: false

  development:
    extends: base  # Using 'extends' instead of 'inherits'
    debug: true
    port: 3000
"""

    config_dir = Path("custom-key-demo")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text(config_content)

    try:
        # This would fail with default inherit_key
        print("Using custom inheritance key 'extends':")

        resolver = ProfileConfigResolver(
            "custom-key-demo", profile="development", inherit_key="extends"
        )
        config = resolver.resolve()

        for key, value in sorted(config.items()):
            print(f"   {key}: {value}")
        print()

    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


if __name__ == "__main__":
    demonstrate_inheritance_chain()
    demonstrate_profile_comparison()
    demonstrate_error_handling()
    demonstrate_custom_inheritance_key()
