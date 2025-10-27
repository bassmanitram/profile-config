# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated testing, code quality, releases, and maintenance of the Profile Config package.

## Workflows Overview

### 🧪 [test.yml](workflows/test.yml) - Core Testing
**Triggers:** Push/PR to main/develop branches

**What it does:**
- Tests across Python 3.8-3.12 on Ubuntu, Windows, and macOS
- Runs full test suite with coverage reporting
- Uploads coverage to Codecov
- Tests all examples to ensure they work

**Matrix:** 15 combinations (3 OS × 5 Python versions)

### 🔍 [lint.yml](workflows/lint.yml) - Code Quality
**Triggers:** Push/PR to main/develop branches

**What it does:**
- **Code Formatting:** Black formatting checks
- **Import Sorting:** isort checks
- **Linting:** flake8 for code quality
- **Type Checking:** mypy for type safety
- **Security:** bandit for security issues
- **Vulnerability Scanning:** safety for dependency vulnerabilities

### 🚀 [release.yml](workflows/release.yml) - Automated Releases
**Triggers:** Git tags matching `v*` (e.g., `v1.0.0`)

**What it does:**
1. **Build:** Creates source distribution and wheel
2. **Test:** Installs and tests package on all platforms
3. **Publish:** Uploads to PyPI using trusted publishing
4. **Release:** Creates GitHub release with changelog

**Security:** Uses OpenID Connect trusted publishing (no API keys needed)

### 📚 [docs.yml](workflows/docs.yml) - Documentation
**Triggers:** Push to main, PR to main

**What it does:**
- Generates API documentation with Sphinx
- Builds HTML documentation
- Deploys to GitHub Pages (on main branch)
- Creates downloadable documentation artifacts

### 🔄 [dependency-update.yml](workflows/dependency-update.yml) - Dependency Management
**Triggers:** Weekly schedule (Mondays 9 AM UTC), manual dispatch

**What it does:**
- Updates all dependencies to latest compatible versions
- Runs security vulnerability checks
- Creates automated PR with updates
- Tests updated dependencies before merging

### 🔧 [compatibility.yml](workflows/compatibility.yml) - Compatibility Testing
**Triggers:** Monthly schedule (1st of month 6 AM UTC), manual dispatch

**What it does:**
- Tests against Python development versions (3.13-dev)
- Tests minimum vs latest dependency versions
- Tests optional dependency scenarios
- Ensures backward compatibility

## Workflow Status Badges

Add these to your README.md:

```markdown
[![Tests](https://github.com/bassmanitram/profile-config/workflows/Tests/badge.svg)](https://github.com/bassmanitram/profile-config/actions/workflows/test.yml)
[![Code Quality](https://github.com/bassmanitram/profile-config/workflows/Code%20Quality/badge.svg)](https://github.com/bassmanitram/profile-config/actions/workflows/lint.yml)
[![Documentation](https://github.com/bassmanitram/profile-config/workflows/Documentation/badge.svg)](https://github.com/bassmanitram/profile-config/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/bassmanitram/profile-config/branch/main/graph/badge.svg)](https://codecov.io/gh/bassmanitram/profile-config)
[![PyPI version](https://badge.fury.io/py/profile-config.svg)](https://badge.fury.io/py/profile-config)
```

## Setup Requirements

### 1. Repository Settings

**Branch Protection (Settings → Branches):**
- Require status checks: `test`, `lint`
- Require branches to be up to date
- Require linear history
- Include administrators

**Pages (Settings → Pages):**
- Source: GitHub Actions
- Enable for documentation deployment

### 2. PyPI Publishing Setup

**Trusted Publishing (Recommended):**
1. Go to [PyPI Trusted Publishers](https://pypi.org/manage/account/publishing/)
2. Add publisher:
   - Owner: `bassmanitram`
   - Repository: `profile-config`
   - Workflow: `release.yml`
   - Environment: `release`

**Alternative - API Token:**
1. Create PyPI API token
2. Add as repository secret: `PYPI_API_TOKEN`
3. Update release.yml to use token instead of trusted publishing

### 3. Codecov Integration

1. Sign up at [Codecov](https://codecov.io/)
2. Connect your GitHub repository: `bassmanitram/profile-config`
3. No additional setup needed (uses GitHub Actions token)

### 4. Environment Secrets

**Repository Secrets (Settings → Secrets and variables → Actions):**
- `GITHUB_TOKEN` - Automatically provided
- `PYPI_API_TOKEN` - Only if not using trusted publishing

**Environment: `release`**
- Used for PyPI publishing
- Can add additional protection rules

## Usage Examples

### Creating a Release

```bash
# Create and push a tag
git tag v1.0.0
git push origin v1.0.0

# This triggers the release workflow automatically
```

### Manual Workflow Triggers

```bash
# Trigger dependency updates
gh workflow run dependency-update.yml

# Trigger compatibility tests
gh workflow run compatibility.yml
```

### Local Development

```bash
# Run the same checks locally
black --check profile_config/ examples/
isort --check-only profile_config/ examples/
flake8 profile_config/ examples/
mypy profile_config/
pytest --cov=profile_config
```

## Best Practices

1. **Keep workflows fast:** Use caching, parallel jobs
2. **Fail fast:** Use `fail-fast: false` only when needed
3. **Security first:** Use trusted publishing, minimal permissions
4. **Monitor regularly:** Check workflow runs and update dependencies
5. **Document changes:** Update this README when modifying workflows