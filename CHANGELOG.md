# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2024-12-04

### Added
- **Global Environment Variable Expansion**: `${env:VAR_NAME}` syntax now works in ANY configuration value
  - Read existing environment variables at configuration evaluation time
  - Syntax: `${env:HOME}`, `${env:USER}`, `${env:PATH}`, etc.
  - Missing variables return `None`/empty string (treated as "not set")
  - Implemented via custom OmegaConf resolver
  - Works in defaults, profiles, nested structures, lists, and env_vars section
  - Combines seamlessly with existing `${...}` interpolation syntax
  
- **Global Command Execution**: `$(command)` syntax now works in ANY configuration value
  - Execute shell commands at configuration evaluation time
  - Syntax: `$(echo value)`, `$(hostname)`, `$(git rev-parse HEAD)`, `$(basename ${PWD})`, etc.
  - Full shell expansion: can use `$VAR`, `${VAR}`, pipes, and complex commands
  - Failed commands (non-zero exit) result in `None` value → key omitted from configuration
  - Empty command output results in `None` value → key omitted from configuration
  - Timeout protection: commands must complete within `command_timeout` seconds (default: 2.0s)
  - Comprehensive error logging via standard Python logging
  - Commands execute with current `os.environ` (can access all environment variables)
  - Works in defaults, profiles, nested structures, lists, and env_vars section
  - New parameter: `command_timeout` (default: 2.0 seconds)

- 20 new comprehensive tests with 99% coverage of new features
  - Environment variable expansion (4 tests)
  - Command execution (8 tests)
  - Combined features (3 tests)
  - Global expansion in all contexts (6 tests)

### Changed
- Command expansion integrated into main resolution pipeline
- Resolution order updated to expand commands before profile resolution
- Commands also expanded in runtime overrides
- Default `command_timeout` set to 2.0 seconds
- Test count increased from 90 to 110 tests
- Coverage maintained at 98%

### Examples

**Environment Variable Expansion**:
```yaml
defaults:
  user: "${env:USER}"
  home: "${env:HOME}"
  project_path: "${env:HOME}/projects/myapp"
```

**Command Execution**:
```yaml
defaults:
  hostname: "$(hostname)"
  git_commit: "$(git rev-parse HEAD)"
  git_branch: "$(git branch --show-current)"
  project_name: "$(basename ${PWD})"
  build_date: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

**Combined Usage**:
```yaml
defaults:
  app_name: myapp
  environment: "$(echo production)"
  deployment_id: "${app_name}_${environment}_$(git rev-parse --short HEAD)"
  
  database:
    host: "db.$(hostname)"
    name: "$(basename ${PWD})_db"
    user: "${env:USER}"
  
  servers:
    - "web1.$(hostname)"
    - "web2.$(hostname)"
```

**In Profiles**:
```yaml
profiles:
  development:
    environment: "$(echo dev)"
    debug_host: "debug.$(hostname)"
  
  production:
    environment: "$(echo prod)"
    server: "prod.$(hostname)"
```

### Security
- Command execution introduces security risks if configuration files are untrusted
- Commands run with `shell=True` enabling full shell features including pipes and variable expansion
- Users are responsible for ensuring configuration files are from trusted sources
- Timeout protection prevents runaway commands (configurable, default 2 seconds)
- All command executions logged at DEBUG level for audit trails
- Failed commands don't crash resolution, they log errors and omit the value

### Technical Details
- Modified `profile_config/merger.py` (+8 lines)
  - Added `__init__()` method
  - Registered custom OmegaConf resolver for `${env:VAR}` syntax
- Modified `profile_config/resolver.py` (+70 lines)
  - Added `command_timeout` parameter
  - Added `_expand_value()` method for single value expansion
  - Added `_expand_commands_recursive()` method for recursive config tree processing
  - Updated `resolve()` to expand commands before profile resolution
  - Updated `resolve()` to expand commands in override sources
- Added `profile_config/tests/test_env_expansion.py` (318 lines, 20 tests)
  - Comprehensive test coverage for both features
  - Platform-specific tests (Unix/Windows)
  - Edge cases: failures, timeouts, empty output, nested structures

### Backward Compatibility
- 100% backward compatible
- Only affects configurations using `${env:...}` or `$(...)` syntax
- Existing configurations work unchanged
- No migration required

## [1.3.0] - 2025-11-13

## [1.3.1] - 2024-12-04

### Added
- **Global Environment Variable Expansion**: `${env:VAR_NAME}` syntax now works in ANY configuration value
  - Read existing environment variables at configuration evaluation time
  - Syntax: `${env:HOME}`, `${env:USER}`, `${env:PATH}`, etc.
  - Missing variables return `None`/empty string (treated as "not set")
  - Implemented via custom OmegaConf resolver
  - Works in defaults, profiles, nested structures, lists, and env_vars section
  - Combines seamlessly with existing `${...}` interpolation syntax
  
- **Global Command Execution**: `$(command)` syntax now works in ANY configuration value
  - Execute shell commands at configuration evaluation time
  - Syntax: `$(echo value)`, `$(hostname)`, `$(git rev-parse HEAD)`, `$(basename ${PWD})`, etc.
  - Full shell expansion: can use `$VAR`, `${VAR}`, pipes, and complex commands
  - Failed commands (non-zero exit) result in `None` value → key omitted from configuration
  - Empty command output results in `None` value → key omitted from configuration
  - Timeout protection: commands must complete within `command_timeout` seconds (default: 2.0s)
  - Comprehensive error logging via standard Python logging
  - Commands execute with current `os.environ` (can access all environment variables)
  - Works in defaults, profiles, nested structures, lists, and env_vars section
  - New parameter: `command_timeout` (default: 2.0 seconds)

- **20 new comprehensive tests** covering both features with 99% test coverage
  - Environment variable expansion tests (4 tests)
  - Command execution tests (8 tests)
  - Combined feature tests (3 tests)
  - Global expansion tests (6 tests): profiles, nesting, interpolation, error handling
  - Platform-specific tests for Unix and Windows compatibility

### Changed
- Command expansion now happens **before** OmegaConf interpolation in resolution pipeline
- Resolution order updated:
  1. Discover and load config files
  2. Merge config files
  3. **→ Expand command substitutions globally** (NEW)
  4. Resolve profile with inheritance
  5. **→ Expand commands in overrides** (NEW)
  6. Apply overrides and OmegaConf interpolation
  7. Apply environment variables to `os.environ`
- Test count increased from 90 to 110 tests
- Coverage maintained at 98%

### Security
- Command execution introduces security risks if configuration files are untrusted
- Commands run with `shell=True` enabling full shell features
- Users are responsible for ensuring configuration files are from trusted sources
- Timeout protection prevents runaway commands (default 2 seconds)
- Failed commands logged but don't crash configuration resolution
- All command executions logged at DEBUG level for audit trails

### Examples

**Environment Variable Expansion**:
```yaml
defaults:
  user: "${env:USER}"
  home: "${env:HOME}"
  project_path: "${env:HOME}/projects/myapp"
```

**Command Execution**:
```yaml
defaults:
  hostname: "$(hostname)"
  git_commit: "$(git rev-parse HEAD)"
  git_branch: "$(git branch --show-current)"
  project_name: "$(basename ${PWD})"
  build_date: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

**Combined Usage**:
```yaml
defaults:
  app_name: myapp
  environment: "$(echo production)"
  
  # Combines all three: config vars, env expansion, and commands
  deployment_id: "${app_name}_${environment}_$(git rev-parse --short HEAD)"
  
  database:
    host: "db.$(hostname)"
    name: "$(basename ${PWD})_db"
    user: "${env:USER}"
  
  servers:
    - "web1.$(hostname)"
    - "web2.$(hostname)"
```

**In Profiles**:
```yaml
profiles:
  development:
    api_url: "http://localhost:8000"
    log_level: "$(echo DEBUG)"
  
  production:
    api_url: "https://api.$(hostname)"
    log_level: "$(echo WARNING)"
```

### Backward Compatibility
- 100% backward compatible
- Existing configurations without `${env:...}` or `$(...)` syntax work unchanged
- Only affects configurations that use the new syntax patterns
- No migration required

## [1.3.0] - 2025-11-13

### Added
- **Environment Variable Injection**: Automatically set environment variables from configuration using the `env_vars` section
  - New `env_vars` configuration section for defining environment variables that are set when configuration is resolved
  - Variables are set in `os.environ` automatically during `resolve()`
  - Supports variable interpolation in environment variable values using `${...}` syntax
  - Profile-aware: environment variables merge with profile overrides following standard precedence rules
  - Type conversion: non-string values (integers, booleans, floats, null) automatically converted to strings
  - Safe by default: existing environment variables are not overwritten (respects container orchestration and CI/CD injected values)
  - The `env_vars` section is automatically removed from the returned configuration dictionary
- New configuration parameters for `ProfileConfigResolver`:
  - `apply_environment` (default: `True`): Enable/disable environment variable application
  - `environment_key` (default: `"env_vars"`): Customize the configuration key name for environment variables
  - `override_environment` (default: `False`): Control whether to override existing environment variables
- New method: `get_environment_info()` returns dictionary with `applied` and `skipped` environment variables for observability
- Comprehensive documentation section in README: "Environment Variables"
  - Basic usage examples
  - Variable interpolation examples
  - Profile-specific environment variables
  - Safe mode and override mode documentation
  - Type conversion reference
  - Use cases: Application Bootstrap, Container Orchestration, Development Environment
  - Security considerations and best practices
- New example script: `examples/env_vars_example.py` demonstrating all environment variable features
- Updated API Reference section in README with new parameters and method

### Changed
- Enhanced `ProfileConfigResolver` with environment variable handling
- Updated GitHub Actions examples workflow to test new example
- Updated README Examples section to include `env_vars_example.py`

### Technical Details
- Modified `profile_config/resolver.py` (98 lines added)
- Added `_apply_environment_variables()` method to extract and apply environment variables
- Added environment tracking attributes: `_env_applied` and `_env_skipped`
- Added 12 comprehensive test cases in `profile_config/tests/test_env_vars.py`:
  - Basic environment variable application
  - Variable interpolation in env_vars
  - Profile-specific environment variables
  - Safe mode (respecting existing variables)
  - Override mode (forcing config values)
  - Disabling the feature
  - Custom key names
  - Runtime overrides with interpolation
  - Type conversion
  - Empty/missing/invalid env_vars sections
- Test coverage maintained at 98%
- Total tests increased from 78 to 90
- All code properly formatted (black, isort) and linted (flake8)

### Security
- Safe default behavior: `override_environment=False` prevents overwriting existing environment variables
- Respects secrets injected by container orchestration or CI/CD systems
- Documentation emphasizes not committing sensitive values to configuration files
- Recommends using secret management systems for credentials

### Backward Compatibility
- 100% backward compatible
- Feature is enabled by default but only activates if `env_vars` section is present in configuration
- Existing configurations without `env_vars` section continue to work unchanged
- All new parameters are optional with safe defaults
- No migration required

## [1.2.0] - 2025-11-12

### Added
- **Automatic Default Profile Creation**: The "default" profile is now automatically created when requested but not explicitly defined in the configuration
  - When `profile="default"` is specified and no explicit default profile exists, returns only the values from the `defaults` section
  - Explicit default profiles still work as before (backward compatible)
  - Eliminates the need to add `default: {}` to every configuration file
  - Makes `profile="default"` intuitive for getting base configuration
- New documentation section in README: "Using the Default Profile"
  - Explains automatic creation behavior
  - Documents explicit default profile usage
  - Provides three practical use cases with examples
- New example script: `examples/default_profile_usage.py`
  - Demonstrates auto-creation of default profile
  - Shows explicit default profile with inheritance
  - Illustrates using default as environment fallback

### Changed
- Enhanced `ProfileResolver.resolve_profile()` to handle missing "default" profile gracefully
- Updated README with comprehensive default profile documentation (98 new lines)
- Added debug logging when auto-creating default profile
- Updated GitHub Actions workflow to use `softprops/action-gh-release@v2` (was v1)
- Code style improvements and formatting consistency

### Technical Details
- Modified `profile_config/profiles.py` (12 lines added)
- Added 3 comprehensive test cases in `profile_config/tests/test_resolver.py`:
  - `test_default_profile_auto_creation`
  - `test_explicit_default_profile_takes_precedence`
  - `test_non_default_profile_still_raises_error`
- Test coverage maintained at 98%
- Total tests increased from 75 to 78
- Merged PR #6: Dependabot update for GitHub Actions

### Backward Compatibility
- 100% backward compatible
- Explicit default profiles continue to work unchanged
- Only affects behavior when "default" profile is requested but not defined
- Non-default profiles still raise `ProfileNotFoundError` if not found

### Use Cases Enabled
1. Base configuration without environment-specific overrides
2. Environment fallback pattern: `os.environ.get("ENV", "default")`
3. Testing with minimal configuration
4. Simplified local development setup

## [1.1.0] - 2025-10-29

### Added
- **Flexible Overrides**: Enhanced `overrides` parameter to accept multiple formats
  - Single dictionary (original behavior, backward compatible)
  - File path (yaml, json, toml)
  - List of dictionaries and/or file paths
  - Overrides applied in order with proper precedence
- **Custom Profile Filename**: New `profile_filename` parameter for `ProfileConfigResolver`
  - Allows using custom filenames instead of hardcoded "config"
  - Default: "config" (maintains backward compatibility)
  - Example: `profile_filename="settings"` searches for `settings.yaml` instead of `config.yaml`
  - Useful for organization standards, multiple config types, and legacy system compatibility
- Comprehensive test suite for new features (29 new tests)
- Feature documentation: `FLEXIBLE_OVERRIDES.md` and `PROFILE_FILENAME_FEATURE.md`

### Changed
- **README.md**: Complete rewrite for clarity and user focus
  - Removed marketing language and superlatives
  - Added visual configuration flow diagram
  - Added concrete examples with expected outputs
  - Clarified precedence and resolution order throughout
  - Improved section organization and navigation
  - Fixed incorrect home directory path references (`~/.myapp/` → `~/myapp/`)
  - Added documentation for new features
- Updated API documentation with new parameters
- Enhanced error messages to include custom profile filename when applicable

### Fixed
- Corrected home directory search path documentation (was showing hidden directory incorrectly)

### Technical Details
- `ProfileConfigResolver.__init__()` now accepts `profile_filename` parameter
- `ConfigDiscovery.__init__()` now accepts `profile_filename` parameter
- New `ProfileConfigResolver._process_overrides()` method for flexible override handling
- Type aliases added: `OverrideSource` and `OverridesType`
- Test coverage increased from 93% to 98%
- Total tests increased from 46 to 75

### Backward Compatibility
- 100% backward compatible
- All existing code continues to work without modification
- Default parameter values maintain original behavior

## [1.0.1] - 2025-10-27

### Added
- Initial release of profile-config
- Hierarchical configuration file discovery
- Profile inheritance with circular dependency detection
- Support for YAML, JSON, and TOML configuration files
- Variable interpolation using OmegaConf
- Runtime configuration overrides
- Configurable search patterns and file locations
- Comprehensive test suite
- Documentation and examples
- Error handling with specific exception types

### Features
- `ProfileConfigResolver` main interface
- `ConfigDiscovery` for hierarchical file discovery
- `ProfileResolver` for profile inheritance
- `ConfigMerger` for configuration merging with OmegaConf
- `ConfigLoader` for multiple file format support
- Custom inheritance key support
- Configurable interpolation enable/disable
- Profile listing and configuration file discovery utilities
