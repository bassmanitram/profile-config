# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-10-25

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