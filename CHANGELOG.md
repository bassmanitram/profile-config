# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
