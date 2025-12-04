# Agent Bootstrap - Profile Config Project

## Project Identity

**Project Name:** profile-config  
**Package Name:** `profile_config`  
**Version:** 1.3.0  
**License:** MIT  
**Repository:** https://github.com/bassmanitram/profile-config  
**PyPI:** https://pypi.org/project/profile-config/  
**Python Support:** 3.8, 3.9, 3.10, 3.11, 3.12  

## Project Purpose

Profile Config is a Python library for managing hierarchical configuration files with profile-based inheritance and variable interpolation. It enables applications to maintain multiple configuration profiles (e.g., development, staging, production) with proper precedence, inheritance, and environment-specific overrides.

### Core Concept

The library discovers configuration files in a hierarchical directory structure, merges them with proper precedence, resolves profile inheritance chains, and provides a unified configuration dictionary to the application. Think of it as a sophisticated configuration management system that combines the flexibility of profile-based configurations with hierarchical discovery.

## Architecture Overview

### Modular Design (5 Core Components)

The project follows a clean separation of concerns with each module having a single responsibility:

1. **ProfileConfigResolver** (`resolver.py`) - Main API facade that orchestrates all operations
2. **ConfigDiscovery** (`discovery.py`) - Hierarchical file discovery across directory tree
3. **ConfigLoader** (`loader.py`) - Multi-format file loading (YAML, JSON, TOML)
4. **ProfileResolver** (`profiles.py`) - Profile inheritance resolution with cycle detection
5. **ConfigMerger** (`merger.py`) - Configuration merging with OmegaConf interpolation

### Configuration Flow

```
User Request → ProfileConfigResolver
    ↓
ConfigDiscovery → Finds config files in hierarchy
    ↓
ConfigLoader → Loads and parses files
    ↓
ConfigMerger → Merges files (most specific wins)
    ↓
ProfileResolver → Resolves profile + inheritance
    ↓
ConfigMerger → Applies overrides + interpolation
    ↓
Apply environment variables → Sets os.environ
    ↓
Final Configuration Dictionary
```

### File Discovery Pattern

Searches upward from CWD, then home directory:
```
./myapp/config.yaml          <- Current directory (highest precedence)
../myapp/config.yaml         <- Parent directory
../../myapp/config.yaml      <- Grandparent directory
~/myapp/config.yaml          <- Home directory (lowest precedence)
```

Pattern: `{config_name}/{profile_filename}.{extension}`

Extensions searched: `.yaml`, `.yml`, `.json`, `.toml`

## Key Features

1. **Hierarchical Discovery**: Walks up directory tree finding configuration files
2. **Profile Inheritance**: Profiles can inherit from other profiles (with cycle detection)
3. **Variable Interpolation**: Uses OmegaConf for `${variable}` substitution
4. **Flexible Overrides**: Runtime overrides from dict, file path, or list of both
5. **Custom Profile Filename**: Use any filename instead of hardcoded "config"
6. **Environment Variable Injection**: Automatically set `os.environ` from config
7. **Multi-Format Support**: YAML, JSON, TOML (with optional tomli for Python < 3.11)
8. **Automatic Default Profile**: "default" profile auto-created if not defined

## Project Structure

```
profile-config/
├── profile_config/          # Main package
│   ├── __init__.py          # Package exports and version
│   ├── resolver.py          # Main API (ProfileConfigResolver)
│   ├── discovery.py         # ConfigDiscovery - file finding
│   ├── loader.py            # ConfigLoader - multi-format parsing
│   ├── profiles.py          # ProfileResolver - inheritance
│   ├── merger.py            # ConfigMerger - merging with OmegaConf
│   ├── exceptions.py        # Custom exceptions
│   └── tests/               # Test suite (2308 lines, 90 tests)
│       ├── test_resolver.py
│       ├── test_discovery.py
│       ├── test_profiles.py
│       ├── test_flexible_overrides.py
│       ├── test_profile_filename.py
│       ├── test_env_vars.py
│       └── test_toml_support.py
├── examples/                # Working examples (6 files)
│   ├── basic_usage.py
│   ├── advanced_profiles.py
│   ├── default_profile_usage.py
│   ├── web_app_config.py
│   ├── env_vars_example.py
│   └── toml_usage.py
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # Architectural documentation
│   └── research/            # Implementation research notes
├── .github/workflows/       # CI/CD (8 workflows)
│   ├── test.yml             # Multi-platform testing
│   ├── lint.yml             # Code quality checks
│   ├── quality.yml          # Security scanning
│   ├── examples.yml         # Example validation
│   ├── docs.yml             # Documentation validation
│   ├── dependencies.yml     # Dependency checks
│   ├── status.yml           # Project health
│   └── release.yml          # Automated releases
├── pyproject.toml           # Project metadata and build config
├── requirements.txt         # Dependencies
├── pytest.ini               # Pytest configuration
├── .flake8                  # Flake8 linting rules
├── .pre-commit-config.yaml  # Pre-commit hooks
├── README.md                # Comprehensive user documentation
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
└── LICENSE                  # MIT License

```

## Dependencies

### Core Dependencies
- **omegaconf>=2.3.0** - Configuration merging and variable interpolation
- **pyyaml>=6.0** - YAML file parsing

### Optional Dependencies
- **tomli>=2.0.0** (Python < 3.11) - TOML support

### Development Dependencies
- **pytest>=6.0**, **pytest-cov>=3.0.0** - Testing
- **black>=22.0.0**, **isort>=5.0.0** - Code formatting
- **flake8>=4.0.0** - Linting
- **mypy>=0.991** - Type checking
- **bandit>=1.7.0** - Security scanning
- **pre-commit>=3.0.0** - Pre-commit hooks
- **build>=0.8.0** - Package building

## Code Quality Standards

### Formatting
- **Black**: Line length 88, target Python 3.8
- **Isort**: Black-compatible profile, line length 88
- **Flake8**: Max line length 120, excludes tests from some rules

### Type Checking
- **Mypy**: Enabled but non-blocking (11 pre-existing errors to fix)
- Type hints used throughout public API
- `types-PyYAML>=6.0.0` for YAML type stubs

### Testing
- **Test Count**: 90 tests across 7 test modules
- **Coverage**: 98% (maintained consistently)
- **Approach**: Pytest with fixtures, temporary directories, context managers
- **Testing Style**: Comprehensive unit + integration tests

### Security
- **Bandit**: Security scanning for vulnerabilities
- **Pre-commit**: 13 hooks for validation and safety

## Configuration File Format

### Standard Structure

```yaml
# Optional: specify default profile
default_profile: development

# Optional: values applied to all profiles
defaults:
  timeout: 30
  retries: 3

# Required: profile definitions
profiles:
  development:
    debug: true
    database: myapp_dev

  production:
    debug: false
    database: myapp_prod
```

### Special Sections

1. **defaults**: Base configuration merged into all profiles
2. **profiles**: Named configuration sets
3. **default_profile**: Which profile to use by default
4. **env_vars**: Environment variables to set in `os.environ`

### Profile Inheritance

```yaml
profiles:
  base:
    host: localhost
    timeout: 30

  development:
    inherits: base    # Inherits from base profile
    debug: true

  staging:
    inherits: development  # Inherits from development (which inherits base)
    debug: false
```

## Common Usage Patterns

### Basic Usage

```python
from profile_config import ProfileConfigResolver

resolver = ProfileConfigResolver("myapp", profile="development")
config = resolver.resolve()

# Access configuration
timeout = config["timeout"]
debug = config["debug"]
```

### With Runtime Overrides

```python
resolver = ProfileConfigResolver(
    "myapp",
    profile="production",
    overrides={"debug": True, "host": "test-server"}
)
config = resolver.resolve()
```

### Environment Variable Injection

```python
# Configuration file includes:
# defaults:
#   env_vars:
#     DATABASE_URL: "postgresql://localhost/mydb"

resolver = ProfileConfigResolver("myapp", profile="development")
config = resolver.resolve()

# os.environ["DATABASE_URL"] is now set automatically
```

### Custom Profile Filename

```python
# Search for settings.yaml instead of config.yaml
resolver = ProfileConfigResolver(
    "myapp",
    profile="development",
    profile_filename="settings"
)
```

## API Reference

### ProfileConfigResolver

**Constructor Parameters:**
- `config_name: str` - Name of configuration directory (required)
- `profile: str = "default"` - Profile name to resolve
- `profile_filename: str = "config"` - Name of profile file without extension
- `overrides: Optional[Union[Dict, PathLike, List[Union[Dict, PathLike]]]]` - Runtime overrides
- `extensions: Optional[List[str]]` - File extensions to search (default: yaml, yml, json, toml)
- `search_home: bool = True` - Whether to search home directory
- `inherit_key: str = "inherits"` - Key name for profile inheritance
- `enable_interpolation: bool = True` - Enable variable interpolation
- `apply_environment: bool = True` - Apply env_vars section to os.environ
- `environment_key: str = "env_vars"` - Key name for environment variables
- `override_environment: bool = False` - Override existing environment variables

**Key Methods:**
- `resolve() -> Dict[str, Any]` - Main method to resolve configuration
- `list_profiles() -> List[str]` - List available profiles
- `get_config_files() -> List[Path]` - Get discovered configuration files
- `get_environment_info() -> Dict[str, Dict[str, str]]` - Get applied/skipped env vars

### Custom Exceptions

All inherit from `ProfileConfigError`:
- `ConfigNotFoundError` - No configuration files found
- `ProfileNotFoundError` - Requested profile doesn't exist
- `CircularInheritanceError` - Circular inheritance detected
- `ConfigFormatError` - Invalid configuration file format

## Development Workflow

### Setup Development Environment

```bash
git clone https://github.com/bassmanitram/profile-config.git
cd profile-config
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev,test,toml]"
```

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=profile_config --cov-report=html

# Specific test file
pytest profile_config/tests/test_resolver.py

# Coverage maintained at 98%
```

### Code Quality Checks

```bash
# Format code
black profile_config/ examples/
isort profile_config/ examples/

# Lint
flake8 profile_config/ examples/

# Type check (has 11 known issues)
mypy profile_config/

# Security scan
bandit -r profile_config/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Running Examples

```bash
cd examples
python basic_usage.py
python advanced_profiles.py
python web_app_config.py
python toml_usage.py
python env_vars_example.py
python default_profile_usage.py
```

## CI/CD Pipeline

### GitHub Actions Workflows

1. **test.yml** - Multi-platform testing
   - Matrix: 3 OS (Ubuntu, Windows, macOS) × 5 Python (3.8-3.12) = 15 environments
   - Runs: black, isort, flake8, pytest with coverage
   - Uploads coverage to Codecov

2. **lint.yml** - Code quality enforcement
   - Black formatting check
   - Isort import sorting
   - Flake8 linting
   - Package build validation
   - Mypy type checking (non-blocking)

3. **examples.yml** - Example validation
   - Tests all 6 examples on Python 3.8, 3.10, 3.12
   - Ensures user-facing code works

4. **quality.yml** - Enhanced quality checks
   - Pre-commit hooks
   - Bandit security scanning
   - Package installation testing

5. **docs.yml** - Documentation validation
   - Validates documentation structure
   - Tests code examples compile
   - Checks cross-references

6. **dependencies.yml** - Weekly dependency checks
   - Security vulnerability scanning
   - Outdated package detection

7. **status.yml** - Daily project health monitoring
   - Comprehensive test runs
   - Code quality checks
   - Package health report

8. **release.yml** - Automated releases
   - Builds package
   - Tests on 15 environments
   - Publishes to PyPI via trusted publishing
   - Creates GitHub release with changelog

### Dependabot

Configured for automatic dependency updates:
- Python packages: Weekly on Mondays
- GitHub Actions: Weekly on Mondays
- Auto-assigns to bassmanitram

## Recent Changes (Version History)

### v1.3.0 (2025-11-13) - Environment Variable Injection
- Added `env_vars` configuration section for automatic `os.environ` setup
- Variable interpolation in environment variables
- Safe mode: respects existing environment variables by default
- Override mode available with `override_environment=True`
- New method: `get_environment_info()` for observability
- 12 new tests added (total: 90 tests)
- Coverage maintained at 98%

### v1.2.0 (2025-11-12) - Automatic Default Profile
- "default" profile auto-created when requested but not defined
- Returns only `defaults` section when auto-created
- Explicit default profiles still work (backward compatible)
- 3 new tests added
- New example: `default_profile_usage.py`

### v1.1.0 (2025-10-29) - Flexible Overrides & Custom Filename
- Enhanced `overrides` parameter: dict, file path, or list of both
- New `profile_filename` parameter for custom filenames
- 29 new tests added
- Complete README rewrite for clarity
- Coverage increased to 98%

### v1.0.1 (2025-10-27) - Initial Release
- Core functionality: hierarchical discovery, profile inheritance
- Multi-format support: YAML, JSON, TOML
- Variable interpolation with OmegaConf
- Comprehensive test suite (46 tests)

## Testing Strategy

### Test Organization (2308 lines across 7 modules)

- **test_resolver.py** (458 lines) - Main API integration tests
- **test_env_vars.py** (409 lines) - Environment variable feature tests
- **test_flexible_overrides.py** (392 lines) - Override functionality tests
- **test_profile_filename.py** (428 lines) - Custom filename feature tests
- **test_discovery.py** (243 lines) - File discovery tests
- **test_profiles.py** (232 lines) - Profile inheritance tests
- **test_toml_support.py** (145 lines) - TOML format tests

### Testing Approach

- **Fixtures**: Temporary directories with sample config files
- **Context Managers**: Safe directory changing for discovery tests
- **Isolation**: Each test creates its own temporary environment
- **Coverage**: Edge cases, error conditions, platform differences
- **Integration**: End-to-end configuration resolution tests

### Example Test Pattern

```python
def test_something(tmp_path):
    """Test description."""
    # Create test configuration
    config_dir = tmp_path / "myapp"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text("""
        defaults:
          key: value
        profiles:
          dev:
            debug: true
    """)
    
    # Test with temporary directory
    with chdir_context(tmp_path):
        resolver = ProfileConfigResolver("myapp", profile="dev")
        config = resolver.resolve()
        assert config["debug"] is True
```

## Known Issues

### Mypy Type Errors (Non-Blocking)
- **Count**: 11 errors across 5 files
- **Status**: Pre-existing, not blocking CI/CD
- **Mitigation**: Mypy set to `continue-on-error: true` in CI
- **Files**: discovery.py, profiles.py, loader.py, merger.py, resolver.py
- **Impact**: None - tests pass, functionality correct

## Important Notes for AI Agents

### When Modifying Code

1. **Run tests after changes**: `pytest --cov=profile_config`
2. **Maintain 98% coverage**: Add tests for new features
3. **Format before commit**: `black . && isort .`
4. **Check linting**: `flake8 profile_config/ examples/`
5. **Update CHANGELOG.md**: Document changes following Keep a Changelog format
6. **Update README.md**: User-facing changes need documentation

### File Locations

- **Source**: `profile_config/*.py` (7 modules)
- **Tests**: `profile_config/tests/test_*.py` (7 test modules)
- **Examples**: `examples/*.py` (6 working examples)
- **Docs**: `README.md` (comprehensive), `docs/ARCHITECTURE.md`, `CONTRIBUTING.md`

### Do Not Modify

- `.venv/` - Virtual environment (huge, excluded from git)
- `dist/` - Build artifacts
- `htmlcov/` - Coverage reports
- `.git/` - Version control
- `*.egg-info/` - Package metadata

### Git Workflow

- **Main branch**: Production-ready code
- **Develop branch**: Integration branch
- **Feature branches**: Named `feature/*`
- **Release workflow**: Triggered by version tags (e.g., `v1.3.0`)

## Build and Release

### Building Package

```bash
python -m build
# Creates dist/profile-config-1.3.0.tar.gz and .whl
```

### Testing Package

```bash
pip install dist/profile_config-1.3.0-py3-none-any.whl
python -c "import profile_config; print(profile_config.__version__)"
```

### Release Process (Automated)

1. Update version in `pyproject.toml` and `profile_config/__init__.py`
2. Update `CHANGELOG.md` with changes
3. Commit changes: `git commit -m "Bump version to X.Y.Z"`
4. Create tag: `git tag vX.Y.Z`
5. Push tag: `git push origin vX.Y.Z`
6. GitHub Actions automatically:
   - Tests on 15 environments
   - Builds package
   - Publishes to PyPI
   - Creates GitHub release

## Support and Community

- **GitHub Issues**: https://github.com/bassmanitram/profile-config/issues
- **GitHub Discussions**: https://github.com/bassmanitram/profile-config/discussions
- **Maintainer**: martin.j.bartlett@gmail.com (bassmanitram)

## Success Criteria for Changes

Every contribution must:
- ✓ Function correctly with proper error handling
- ✓ Include passing tests (maintain 98% coverage)
- ✓ Be documented in README if user-facing
- ✓ Follow Black/Isort formatting (line length 88)
- ✓ Pass Flake8 linting
- ✓ Include docstrings for public APIs
- ✓ Maintain backward compatibility (or major version bump)
- ✓ Update CHANGELOG.md

## Quick Reference Commands

```bash
# Setup
pip install -e ".[dev,test,toml]"

# Test
pytest --cov=profile_config

# Format
black . && isort .

# Lint
flake8 profile_config/ examples/

# Pre-commit
pre-commit run --all-files

# Examples
cd examples && python basic_usage.py

# Build
python -m build

# Clean
rm -rf dist/ build/ *.egg-info/ htmlcov/ .pytest_cache/
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-03  
**Project Version**: 1.3.0  
**For**: AI Agent Bootstrap (new session initialization)
