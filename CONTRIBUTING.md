# Contributing to Profile Config

Thank you for your interest in contributing to Profile Config! This document provides guidelines and information for contributors.

## Project Overview

### For AI Agents and Automated Tools

If you're an AI agent or automated development tool working on this project, please read **AGENT_BOOTSTRAP.md** first. This document provides:

- Complete project architecture and component overview
- Detailed module responsibilities and data flow
- Testing strategy and coverage requirements (98% maintained)
- CI/CD pipeline documentation
- Code quality standards and formatting rules
- Quick reference commands for common tasks
- Known issues and important notes for modifications

The bootstrap document is designed to give automated tools comprehensive project context in a single reference, enabling more effective contributions while maintaining project standards.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bassmanitram/profile-config.git
   cd profile-config
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev,toml]
   ```

4. **Verify installation:**
   ```bash
   python -c "import profile_config; print('Installation successful!')"
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=profile_config --cov-report=html

# Run specific test file
pytest profile_config/tests/test_resolver.py

# Run tests with specific markers
pytest -m "not slow"
```

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code
black profile_config/ examples/

# Sort imports
isort profile_config/ examples/

# Lint code
flake8 profile_config/ examples/

# Type checking
mypy profile_config/
```

### Running Examples

Test your changes with the provided examples:

```bash
python examples/basic_usage.py
python examples/advanced_profiles.py
python examples/web_app_config.py
python examples/toml_usage.py
```

## Contribution Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88)
- Use type hints for all public APIs
- Write docstrings for all public functions and classes

### Testing Requirements

- All new features must include tests
- Maintain or improve test coverage (aim for >85%)
- Include both unit tests and integration tests
- Test error conditions and edge cases

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions and classes
- Update examples if adding new features
- Consider adding architecture documentation for significant changes

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add TOML configuration support
fix: handle missing config files gracefully
docs: update README with TOML examples
test: add integration tests for profile inheritance
refactor: simplify config merger logic
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Python version and operating system
- Profile Config version
- Minimal code example that reproduces the issue
- Expected vs. actual behavior
- Full error traceback if applicable

### Feature Requests

For new features, please:

- Check if the feature already exists or is planned
- Describe the use case and motivation
- Provide examples of how the feature would be used
- Consider backward compatibility implications

### Code Contributions

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the guidelines above
3. **Add tests** for your changes
4. **Update documentation** as needed
5. **Run the full test suite** to ensure nothing is broken
6. **Submit a pull request** with a clear description

### Documentation Improvements

- Fix typos and grammar issues
- Improve code examples
- Add missing documentation
- Clarify confusing sections

## Pull Request Process

1. **Create a descriptive title** that summarizes the change
2. **Fill out the PR template** with all requested information
3. **Ensure all tests pass** and coverage is maintained
4. **Address review feedback** promptly and thoroughly
5. **Squash commits** if requested before merging

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated if needed
- [ ] Examples updated if needed
- [ ] Backward compatibility maintained
- [ ] Performance impact considered

## Release Process

Releases follow semantic versioning (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Getting Help

- **Questions**: Open a GitHub Discussion at https://github.com/bassmanitram/profile-config/discussions
- **Bugs**: Open a GitHub Issue at https://github.com/bassmanitram/profile-config/issues
- **Chat**: Join our community discussions

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project maintainers at martin.j.bartlett@gmail.com. All complaints will be reviewed and investigated promptly and fairly.

## Recognition

Contributors will be recognized in:

- CHANGELOG.md for their contributions
- README.md contributors section
- Release notes for significant contributions

Thank you for contributing to Profile Config! 🎉
