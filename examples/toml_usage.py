#!/usr/bin/env python3
"""
TOML configuration format example.

This example demonstrates how to use profile-config with TOML format
configuration files, showcasing TOML-specific syntax and features.
"""

import os
import tempfile
from pathlib import Path

from profile_config import ProfileConfigResolver


def create_toml_config():
    """Create a comprehensive TOML configuration file."""
    toml_content = '''
# TOML Configuration Example
# TOML is a minimal configuration file format that's easy to read

[defaults]
app_name = "myapp"
version = "1.0.0"
debug = false
# Array of allowed hosts
allowed_hosts = ["localhost", "127.0.0.1"]

# Server configuration
[defaults.server]
host = "0.0.0.0"
port = 8000
workers = 1

# Database configuration with nested tables
[defaults.database]
host = "localhost"
port = 5432
name = "myapp_default"
pool_size = 5
timeout = 30

# Feature flags as a table
[defaults.features]
user_registration = true
email_verification = false
social_login = false
api_v2 = false

# Logging configuration
[defaults.logging]
level = "INFO"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
file = "/var/log/myapp.log"

# Multiple server configurations using array of tables
[[defaults.cache_servers]]
name = "redis-1"
host = "localhost"
port = 6379

[[defaults.cache_servers]]
name = "redis-2"
host = "localhost"
port = 6380

# Profile configurations
[profiles.base]
# Base profile for common settings
[profiles.base.server]
host = "0.0.0.0"
workers = 1

[profiles.base.database]
pool_size = 5
timeout = 30

[profiles.base.features]
user_registration = true

# Development profile
[profiles.development]
inherits = "base"
debug = true

[profiles.development.server]
port = 5000
workers = 1

[profiles.development.database]
host = "localhost"
name = "myapp_dev"

[profiles.development.logging]
level = "DEBUG"
file = "/tmp/myapp-dev.log"

[profiles.development.features]
email_verification = true
api_v2 = true

# Staging profile
[profiles.staging]
inherits = "base"

[profiles.staging.server]
port = 8080
workers = 2

[profiles.staging.database]
host = "staging-db.example.com"
name = "myapp_staging"
pool_size = 10

[profiles.staging.logging]
level = "INFO"
file = "/var/log/myapp-staging.log"

[profiles.staging.features]
email_verification = true
social_login = true

# Production profile
[profiles.production]
inherits = "base"

[profiles.production.server]
port = 8000
workers = 4

[profiles.production.database]
host = "prod-db.example.com"
name = "myapp_prod"
pool_size = 20

[profiles.production.logging]
level = "WARNING"
file = "/var/log/myapp-prod.log"

[profiles.production.features]
user_registration = true
email_verification = true
social_login = true
'''
    
    # Create config directory and file
    config_dir = Path("myapp")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.toml"
    config_file.write_text(toml_content)
    
    return config_file


def demonstrate_toml_features():
    """Demonstrate TOML-specific features and syntax."""
    print("=== TOML Configuration Features ===\n")
    
    config_file = create_toml_config()
    
    try:
        # Example 1: Basic TOML loading
        print("1. Loading TOML Configuration:")
        resolver = ProfileConfigResolver("myapp", profile="development", search_home=False)
        config = resolver.resolve()
        
        print(f"   App name: {config['app_name']}")
        print(f"   Debug mode: {config['debug']}")
        print(f"   Server port: {config['server']['port']}")
        print(f"   Database: {config['database']['name']} on {config['database']['host']}")
        print()
        
        # Example 2: Array handling
        print("2. TOML Arrays:")
        print(f"   Allowed hosts: {config['allowed_hosts']}")
        print(f"   Cache servers: {len(config['cache_servers'])} configured")
        for i, server in enumerate(config['cache_servers']):
            print(f"     {i+1}. {server['name']}: {server['host']}:{server['port']}")
        print()
        
        # Example 3: Nested tables
        print("3. TOML Nested Tables:")
        features = config['features']
        print("   Feature flags:")
        for feature, enabled in features.items():
            status = "✅" if enabled else "❌"
            print(f"     {status} {feature}")
        print()
        
        # Example 4: Profile comparison
        print("4. Profile Comparison:")
        profiles = ["development", "staging", "production"]
        
        print("   Database Configuration:")
        print("   Profile      Host                    Database        Pool Size")
        print("   " + "-" * 65)
        
        for profile in profiles:
            resolver = ProfileConfigResolver("myapp", profile=profile, search_home=False)
            config = resolver.resolve()
            db = config['database']
            pool_size = db.get('pool_size', 'N/A')
            print(f"   {profile:<12} {db['host']:<23} {db['name']:<15} {pool_size}")
        print()
        
        # Example 5: TOML vs YAML syntax comparison
        print("5. TOML vs YAML Syntax Comparison:")
        print()
        print("   TOML:")
        print("   ```toml")
        print("   [database]")
        print("   host = \"localhost\"")
        print("   port = 5432")
        print("   ")
        print("   [[cache_servers]]")
        print("   name = \"redis-1\"")
        print("   host = \"localhost\"")
        print("   ```")
        print()
        print("   YAML:")
        print("   ```yaml")
        print("   database:")
        print("     host: localhost")
        print("     port: 5432")
        print("   ")
        print("   cache_servers:")
        print("     - name: redis-1")
        print("       host: localhost")
        print("   ```")
        print()
        
    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_toml_variable_interpolation():
    """Demonstrate variable interpolation with TOML."""
    print("=== TOML Variable Interpolation ===\n")
    
    toml_content = '''
[defaults]
app_name = "myapp"
environment = "development"
base_path = "/opt/${app_name}"
data_path = "${base_path}/data"
log_path = "${base_path}/logs/${environment}"
config_path = "${base_path}/config"

[defaults.database]
name = "${app_name}_${environment}"
url = "sqlite:///${data_path}/app.db"

[profiles.development]
environment = "dev"
base_path = "/tmp/${app_name}"

[profiles.production]
environment = "prod"
base_path = "/var/lib/${app_name}"
'''
    
    config_dir = Path("myapp")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.toml"
    config_file.write_text(toml_content)
    
    try:
        print("Variable interpolation with different profiles:")
        print()
        
        for profile in ["development", "production"]:
            print(f"Profile: {profile}")
            resolver = ProfileConfigResolver("myapp", profile=profile, search_home=False)
            config = resolver.resolve()
            
            print(f"   Base path: {config['base_path']}")
            print(f"   Data path: {config['data_path']}")
            print(f"   Log path: {config['log_path']}")
            print(f"   Database name: {config['database']['name']}")
            print(f"   Database URL: {config['database']['url']}")
            print()
            
    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_toml_data_types():
    """Demonstrate TOML data type support."""
    print("=== TOML Data Types ===\n")
    
    toml_content = '''
[defaults]
# String
app_name = "myapp"
description = """
Multi-line string
with line breaks
"""

# Integer
port = 8000
max_connections = 1000

# Float
timeout = 30.5
cpu_threshold = 0.85

# Boolean
debug = true
ssl_enabled = false

# Arrays
tags = ["web", "api", "python"]
ports = [8000, 8001, 8002]

# Inline tables
database = { host = "localhost", port = 5432, ssl = true }
redis = { host = "localhost", port = 6379 }

# Array of tables
[[servers]]
name = "web1"
ip = "192.168.1.1"
active = true

[[servers]]
name = "web2"
ip = "192.168.1.2"
active = false
'''
    
    config_dir = Path("myapp")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.toml"
    config_file.write_text(toml_content)
    
    try:
        resolver = ProfileConfigResolver("myapp", search_home=False)
        config = resolver.resolve()
        
        print("TOML supports rich data types:")
        print(f"   String: {config['app_name']} ({type(config['app_name']).__name__})")
        print(f"   Integer: {config['port']} ({type(config['port']).__name__})")
        print(f"   Float: {config['timeout']} ({type(config['timeout']).__name__})")
        print(f"   Boolean: {config['debug']} ({type(config['debug']).__name__})")
        print(f"   Array: {config['tags']} ({type(config['tags']).__name__})")
        print(f"   Inline table: {config['database']} ({type(config['database']).__name__})")
        print(f"   Array of tables: {len(config['servers'])} servers")
        
        print("\n   Multi-line string:")
        print(f"   {repr(config['description'])}")
        
        print("\n   Server details:")
        for server in config['servers']:
            status = "🟢" if server['active'] else "🔴"
            print(f"     {status} {server['name']}: {server['ip']}")
        print()
        
    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_toml_error_handling():
    """Demonstrate TOML error handling."""
    print("=== TOML Error Handling ===\n")
    
    # Example 1: Invalid TOML syntax
    print("1. Invalid TOML Syntax:")
    invalid_toml = '''
[defaults
missing_bracket = "this will fail"
'''
    
    config_dir = Path("myapp")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.toml"
    
    try:
        config_file.write_text(invalid_toml)
        
        try:
            resolver = ProfileConfigResolver("myapp", search_home=False)
            config = resolver.resolve()
            print("   ERROR: Should have failed!")
        except Exception as e:
            print(f"   ✅ Caught error: {type(e).__name__}")
            print(f"   Message: {str(e)}")
        print()
        
        # Example 2: Valid TOML, invalid profile
        print("2. Valid TOML, Invalid Profile:")
        valid_toml = '''
[defaults]
app_name = "myapp"

[profiles.development]
debug = true
'''
        
        config_file.write_text(valid_toml)
        
        try:
            resolver = ProfileConfigResolver("myapp", profile="nonexistent", search_home=False)
            config = resolver.resolve()
            print("   ERROR: Should have failed!")
        except Exception as e:
            print(f"   ✅ Caught error: {type(e).__name__}")
            print(f"   Message: {str(e)}")
        print()
        
    finally:
        # Cleanup
        if config_file.exists():
            config_file.unlink()
        if config_dir.exists():
            config_dir.rmdir()


if __name__ == "__main__":
    demonstrate_toml_features()
    demonstrate_toml_variable_interpolation()
    demonstrate_toml_data_types()
    demonstrate_toml_error_handling()