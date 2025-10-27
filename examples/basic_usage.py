#!/usr/bin/env python3
"""
Basic usage example for profile-config.

This example demonstrates the fundamental usage patterns of the profile-config
library for hierarchical configuration management.
"""

import tempfile
import os
from pathlib import Path

from profile_config import ProfileConfigResolver


def create_sample_config():
    """Create a sample configuration file for demonstration."""
    config_content = """
# Default configuration values
defaults:
  database_host: localhost
  database_port: 5432
  timeout: 30
  debug: false

# Profile configurations
profiles:
  # Development profile
  development:
    database_name: myapp_dev
    debug: true
    log_level: DEBUG
    
  # Staging profile inherits from development
  staging:
    inherits: development
    database_name: myapp_staging
    debug: false
    log_level: INFO
    
  # Production profile
  production:
    database_name: myapp_prod
    database_host: prod-db.example.com
    log_level: WARNING
    timeout: 60
"""
    
    # Create config directory and file
    config_dir = Path("myapp")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text(config_content)
    
    print(f"Created sample config at: {config_file.absolute()}")
    return config_file


def demonstrate_basic_usage():
    """Demonstrate basic configuration resolution."""
    print("=== Basic Usage Example ===\n")
    
    # Create sample configuration
    config_file = create_sample_config()
    
    try:
        # Example 1: Resolve development profile
        print("1. Resolving 'development' profile:")
        resolver = ProfileConfigResolver("myapp", profile="development")
        dev_config = resolver.resolve()
        
        for key, value in sorted(dev_config.items()):
            print(f"   {key}: {value}")
        print()
        
        # Example 2: Resolve staging profile (with inheritance)
        print("2. Resolving 'staging' profile (inherits from development):")
        resolver = ProfileConfigResolver("myapp", profile="staging")
        staging_config = resolver.resolve()
        
        for key, value in sorted(staging_config.items()):
            print(f"   {key}: {value}")
        print()
        
        # Example 3: Resolve production profile
        print("3. Resolving 'production' profile:")
        resolver = ProfileConfigResolver("myapp", profile="production")
        prod_config = resolver.resolve()
        
        for key, value in sorted(prod_config.items()):
            print(f"   {key}: {value}")
        print()
        
        # Example 4: List available profiles
        print("4. Available profiles:")
        profiles = resolver.list_profiles()
        for profile in profiles:
            print(f"   - {profile}")
        print()
        
        # Example 5: Using overrides
        print("5. Using runtime overrides:")
        overrides = {
            "database_host": "override-db.example.com",
            "custom_setting": "runtime_value"
        }
        resolver = ProfileConfigResolver("myapp", profile="development", overrides=overrides)
        override_config = resolver.resolve()
        
        for key, value in sorted(override_config.items()):
            print(f"   {key}: {value}")
        print()
        
    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_variable_interpolation():
    """Demonstrate variable interpolation features."""
    print("=== Variable Interpolation Example ===\n")
    
    config_content = """
defaults:
  app_name: myapp
  base_path: /opt/${app_name}
  data_path: ${base_path}/data
  log_path: ${base_path}/logs
  database_url: sqlite:///${data_path}/app.db

profiles:
  development:
    base_path: /tmp/${app_name}
    
  production:
    base_path: /var/lib/${app_name}
    database_url: postgresql://prod-db/${app_name}
"""
    
    # Create config directory and file
    config_dir = Path("interpolation-demo")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text(config_content)
    
    try:
        print("Configuration with variable interpolation:")
        
        # Resolve development profile
        resolver = ProfileConfigResolver("interpolation-demo", profile="development")
        config = resolver.resolve()
        
        for key, value in sorted(config.items()):
            print(f"   {key}: {value}")
        print()
        
    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_hierarchical_discovery():
    """Demonstrate hierarchical configuration file discovery."""
    print("=== Hierarchical Discovery Example ===\n")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        
        try:
            # Create nested directory structure
            base_dir = Path(tmpdir)
            project_dir = base_dir / "project"
            sub_dir = project_dir / "subproject"
            sub_dir.mkdir(parents=True)
            
            # Create base configuration
            base_config_dir = base_dir / "myapp"
            base_config_dir.mkdir()
            base_config = base_config_dir / "config.yaml"
            base_config.write_text("""
defaults:
  level: base
  timeout: 30
  
profiles:
  dev:
    debug: true
""")
            
            # Create project-level configuration
            project_config_dir = project_dir / "myapp"
            project_config_dir.mkdir()
            project_config = project_config_dir / "config.yaml"
            project_config.write_text("""
defaults:
  level: project
  port: 8080
  
profiles:
  dev:
    debug: false
    custom_setting: project_value
""")
            
            # Change to subdirectory
            os.chdir(sub_dir)
            
            print("Directory structure:")
            print(f"   Base: {base_config}")
            print(f"   Project: {project_config}")
            print(f"   Current: {sub_dir}")
            print()
            
            # Resolve configuration (should find both files)
            resolver = ProfileConfigResolver("myapp", profile="dev")
            config = resolver.resolve()
            
            print("Resolved configuration (project overrides base):")
            for key, value in sorted(config.items()):
                print(f"   {key}: {value}")
            print()
            
            # Show discovered files
            files = resolver.get_config_files()
            print("Discovered configuration files (in precedence order):")
            for i, file_path in enumerate(files, 1):
                print(f"   {i}. {file_path}")
            print()
            
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    demonstrate_basic_usage()
    demonstrate_variable_interpolation()
    demonstrate_hierarchical_discovery()