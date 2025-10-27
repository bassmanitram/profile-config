# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated releases and maintenance of the Profile Config package.

## Workflows Overview

### 🚀 [release.yml](workflows/release.yml) - Automated Releases
**Triggers:** Git tags matching `v*` (e.g., `v1.0.0`)

**What it does:**
1. **Build:** Creates source distribution and wheel
2. **Test:** Installs and tests package on multiple Python versions and platforms
3. **Publish:** Uploads to PyPI using trusted publishing
4. **Release:** Creates GitHub release with changelog

**Security:** Uses OpenID Connect trusted publishing (no API keys needed)

**Matrix Testing:** Tests across:
- **Operating Systems:** Ubuntu, Windows, macOS
- **Python Versions:** 3.8, 3.9, 3.10, 3.11, 3.12
- **Total Combinations:** 15 test environments

## Setup Requirements

### 1. PyPI Publishing Setup

**Trusted Publishing (Current Setup):**
1. Go to [PyPI Trusted Publishers](https://pypi.org/manage/account/publishing/)
2. Add publisher:
   - Owner: `bassmanitram`
   - Repository: `profile-config`
   - Workflow: `release.yml`
   - Environment: `release`

### 2. GitHub Environment

**Environment: `release`**
- Used for PyPI publishing
- Configured with deployment protection rules
- Allows deployments from `main` branch and `v*` tags

## Usage Examples

### Creating a Release

```bash
# Create and push a tag
git tag v1.0.2
git push origin v1.0.2

# This triggers the release workflow automatically
```

### Manual Workflow Triggers

```bash
# View workflow runs
gh run list --workflow=release.yml

# Re-run a failed workflow
gh run rerun <run-id>
```

### Local Development Testing

```bash
# Test the same build process locally
python -m build
twine check dist/*

# Test installation
pip install dist/*.whl
python -c "import profile_config; print('Success!')"
```

## Workflow Features

### Build Process
- Creates both source distribution (`.tar.gz`) and wheel (`.whl`)
- Validates package metadata with `twine check`
- Uploads build artifacts for debugging

### Cross-Platform Testing
- Tests package installation on all major platforms
- Verifies imports work correctly
- Uses Python's built-in `glob` for cross-platform compatibility

### Security
- Uses GitHub's trusted publishing (no API tokens stored)
- Minimal required permissions
- Environment protection rules

### Release Creation
- Automatically generates changelog from git commits
- Creates GitHub release with proper versioning
- Links to PyPI package page

## Best Practices

1. **Version Tags:** Use semantic versioning (e.g., `v1.0.2`)
2. **Testing:** Always test locally before creating releases
3. **Changelog:** Write meaningful commit messages for auto-generated changelogs
4. **Security:** Never store API tokens as secrets when using trusted publishing

## Troubleshooting

### Common Issues

1. **PyPI trusted publishing not configured:**
   - Verify publisher settings match exactly
   - Check environment name is `release`

2. **Package validation errors:**
   - Run `python -m build` locally first
   - Check `twine check dist/*` passes

3. **Cross-platform test failures:**
   - Test imports work: `python -c "import profile_config"`
   - Check for platform-specific path issues

### Monitoring

- Check [Actions tab](https://github.com/bassmanitram/profile-config/actions) for workflow status
- Review failed runs for detailed error logs
- Monitor [PyPI package page](https://pypi.org/project/profile-config/) for successful uploads