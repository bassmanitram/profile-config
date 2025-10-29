# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
