# Profile Config

[![PyPI version](https://badge.fury.io/py/profile-config.svg)](https://badge.fury.io/py/profile-config)

Hierarchical profile-based configuration management for Python applications.

Profile Config provides a robust solution for managing application configuration across different environments and deployment scenarios. It supports hierarchical configuration file discovery, profile inheritance, variable interpolation, and runtime overrides.

## Features

- **Hierarchical Discovery**: Automatically discovers configuration files by walking up the directory tree
- **Profile Inheritance**: Profiles can inherit from other profiles with circular dependency detection
- **Multiple Formats**: Supports YAML, JSON, and TOML configuration files
- **Variable Interpolation**: Supports variable substitution using `${variable}` syntax
- **Runtime Overrides**: Apply configuration overrides at runtime
- **Configurable Search**: Customize search patterns and file locations
- **Type Safety**: Built on OmegaConf for robust configuration merging

## Installation

```bash
pip install profile-config
```

For TOML support on Python < 3.11:
```bash
pip install profile-config[toml]
```

## Quick Start

Create a configuration file at `myapp/config.yaml`:

```yaml
defaults:
  database_host: localhost
  database_port: 5432
  debug: false

profiles:
  development:
    debug: true
    database_name: myapp_dev
    
  production:
    database_name: myapp_prod
    database_host: prod-db.example.com
```

Or use TOML format at `myapp/config.toml`:

```toml
[defaults]
database_host = "localhost"
database_port = 5432
debug = false

[profiles.development]
debug = true
database_name = "myapp_dev"

[profiles.production]
database_name = "myapp_prod"
database_host = "prod-db.example.com"
```

Use in your application:

```python
from profile_config import ProfileConfigResolver

# Resolve development profile
resolver = ProfileConfigResolver("myapp", profile="development")
config = resolver.resolve()

print(config["debug"])  # True
print(config["database_host"])  # localhost
print(config["database_name"])  # myapp_dev
```

## Configuration File Discovery

Profile Config uses a hierarchical search strategy to discover configuration files:

1. **Current Directory Tree**: Walks up from current working directory
   - `./myapp/config.{yaml,yml,json,toml}`
   - `../myapp/config.{yaml,yml,json,toml}`
   - `../../myapp/config.{yaml,yml,json,toml}`
   - etc.

2. **Home Directory**: Searches user's home directory
   - `$HOME/myapp/config.{yaml,yml,json,toml}`

Files found in more specific locations (closer to current directory) take precedence over more general ones.

## Supported Configuration Formats

### YAML Format
```yaml
defaults:
  database_host: localhost
  features:
    - user_auth
    - api_v2

profiles:
  development:
    debug: true
```

### JSON Format
```json
{
  "defaults": {
    "database_host": "localhost",
    "features": ["user_auth", "api_v2"]
  },
  "profiles": {
    "development": {
      "debug": true
    }
  }
}
```

### TOML Format
```toml
[defaults]
database_host = "localhost"
features = ["user_auth", "api_v2"]

[profiles.development]
debug = true
```

**TOML Benefits:**
- **Type Safety**: Native support for strings, integers, floats, booleans, dates
- **Readable**: Clean syntax without excessive nesting
- **Standardized**: Official specification with compliant parsers
- **Rich Data Types**: Arrays, inline tables, array of tables

## Profile Inheritance

Profiles support inheritance using the `inherits` key:

```yaml
profiles:
  base:
    database_host: localhost
    timeout: 30
    
  development:
    inherits: base
    debug: true
    database_name: myapp_dev
    
  staging:
    inherits: development
    debug: false
    database_host: staging-db.example.com
```

TOML equivalent:
```toml
[profiles.base]
database_host = "localhost"
timeout = 30

[profiles.development]
inherits = "base"
debug = true
database_name = "myapp_dev"

[profiles.staging]
inherits = "development"
debug = false
database_host = "staging-db.example.com"
```

Inheritance chains are resolved automatically with circular dependency detection.

## Team and Environment Management

Handle team differences and multiple environments using profiles:

```yaml
profiles:
  # Base environment profiles
  development:
    debug: true
    database_name: myapp_dev
    
  production:
    debug: false
    database_name: myapp_prod
    
  # Team-specific profiles
  development-team1:
    inherits: development
    team_id: team1
    custom_endpoint: "https://team1.internal.com"
    
  development-team2:
    inherits: development
    team_id: team2
    custom_endpoint: "https://team2.internal.com"
    
  production-team1:
    inherits: production
    team_id: team1
    workers: 4
    
  production-team2:
    inherits: production
    team_id: team2
    workers: 8
```

Usage with environment variables:

```python
import os
from profile_config import ProfileConfigResolver

# Teams set TEAM_NAME in their environment
team = os.environ.get("TEAM_NAME", "")
env = os.environ.get("ENV", "development")

profile = f"{env}-{team}" if team else env
resolver = ProfileConfigResolver("myapp", profile=profile)
config = resolver.resolve()
```

## Variable Interpolation

Configuration values support variable interpolation:

```yaml
defaults:
  app_name: myapp
  base_path: /opt/${app_name}
  data_path: ${base_path}/data
  log_path: ${base_path}/logs

profiles:
  development:
    base_path: /tmp/${app_name}
```

TOML equivalent:
```toml
[defaults]
app_name = "myapp"
base_path = "/opt/${app_name}"
data_path = "${base_path}/data"
log_path = "${base_path}/logs"

[profiles.development]
base_path = "/tmp/${app_name}"
```

Variables are resolved after profile inheritance is complete.

## Runtime Overrides

Apply configuration overrides at runtime:

```python
overrides = {
    "database_host": "override-db.example.com",
    "debug": True,
    "new_setting": "runtime_value"
}

resolver = ProfileConfigResolver(
    "myapp", 
    profile="production",
    overrides=overrides
)
config = resolver.resolve()
```

## Advanced Usage

### Custom Search Configuration

```python
resolver = ProfileConfigResolver(
    config_name="myapp",
    profile="development",
    extensions=["yaml", "json"],  # Only search these formats
    search_home=False,           # Don't search home directory
)
```

### Custom Inheritance Key

```python
# Use 'extends' instead of 'inherits'
resolver = ProfileConfigResolver(
    "myapp",
    profile="development", 
    inherit_key="extends"
)
```

### Disable Variable Interpolation

```python
resolver = ProfileConfigResolver(
    "myapp",
    profile="development",
    enable_interpolation=False
)
```

### List Available Profiles

```python
resolver = ProfileConfigResolver("myapp")
profiles = resolver.list_profiles()
print(f"Available profiles: {profiles}")
```

### Get Discovered Files

```python
resolver = ProfileConfigResolver("myapp")
files = resolver.get_config_files()
for file_path in files:
    print(f"Found config: {file_path}")
```

## Configuration File Format

Configuration files support the following structure:

```yaml
# Optional: specify default profile name
default_profile: development

# Optional: global defaults applied to all profiles
defaults:
  timeout: 30
  retries: 3
  
# Profile definitions
profiles:
  base:
    database_host: localhost
    cache_enabled: true
    
  development:
    inherits: base  # Optional: inherit from another profile
    debug: true
    database_name: myapp_dev
    
  production:
    inherits: base
    database_host: prod-db.example.com
    database_name: myapp_prod
    cache_ttl: 3600
```

## Format Comparison

| Feature | YAML | JSON | TOML |
|---------|------|------|------|
| **Readability** | ✅ Excellent | ⚠️ Good | ✅ Excellent |
| **Comments** | ✅ Yes | ❌ No | ✅ Yes |
| **Multi-line strings** | ✅ Yes | ⚠️ Escaped | ✅ Yes |
| **Type safety** | ⚠️ Inferred | ⚠️ Limited | ✅ Native |
| **Nesting** | ✅ Natural | ✅ Natural | ⚠️ Verbose |
| **Arrays** | ✅ Clean | ✅ Standard | ✅ Clean |
| **Ecosystem** | ✅ Mature | ✅ Universal | ⚠️ Growing |

**Recommendations:**
- **YAML**: Best for complex nested configurations
- **JSON**: Best for API integration and data exchange
- **TOML**: Best for application configuration with type safety

## Error Handling

Profile Config provides specific exceptions for different error conditions:

```python
from profile_config import ProfileConfigResolver
from profile_config.exceptions import (
    ConfigNotFoundError,
    ProfileNotFoundError, 
    CircularInheritanceError,
    ConfigFormatError
)

try:
    resolver = ProfileConfigResolver("myapp", profile="nonexistent")
    config = resolver.resolve()
except ConfigNotFoundError:
    print("No configuration files found")
except ProfileNotFoundError as e:
    print(f"Profile not found: {e}")
except CircularInheritanceError as e:
    print(f"Circular inheritance detected: {e}")
except ConfigFormatError as e:
    print(f"Configuration format error: {e}")
```

## Examples

The `examples/` directory contains comprehensive examples:

- `basic_usage.py`: Basic configuration resolution and profile usage
- `advanced_profiles.py`: Complex inheritance patterns and error handling
- `web_app_config.py`: Real-world web application configuration management
- `toml_usage.py`: TOML format features and syntax examples

Run examples:

```bash
cd examples
python basic_usage.py
python advanced_profiles.py
python web_app_config.py
python toml_usage.py
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/bassmanitram/profile-config.git
cd profile-config
pip install -e ".[dev,toml]"
```

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=profile_config --cov-report=html
```

### Code Formatting

```bash
black profile_config/ examples/
isort profile_config/ examples/
```

### Type Checking

```bash
mypy profile_config/
```

## License

MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and submit pull requests to the [main repository](https://github.com/bassmanitram/profile-config).

## Links

- **GitHub Repository**: https://github.com/bassmanitram/profile-config
- **PyPI Package**: https://pypi.org/project/profile-config/
- **Documentation**: https://bassmanitram.github.io/profile-config/
- **Issue Tracker**: https://github.com/bassmanitram/profile-config/issues

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.