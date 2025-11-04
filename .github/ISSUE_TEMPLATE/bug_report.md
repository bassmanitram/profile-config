---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

## Bug Description
A clear and concise description of what the bug is.

## Reproduction Steps
Steps to reproduce the behavior:
1. Create configuration file with '...'
2. Use ProfileConfigResolver with '...'
3. Call resolve() with '...'
4. See error

## Expected Behavior
A clear and concise description of what you expected to happen.

## Actual Behavior
A clear and concise description of what actually happened.

## Minimal Example
```python
from profile_config import ProfileConfigResolver

# Your minimal reproduction case here
resolver = ProfileConfigResolver(
    config_dir='myapp',
    profile='production'
)
config = resolver.resolve()
```

## Configuration File
If applicable, provide the configuration file(s) used:

```yaml
# config.yaml
defaults:
  setting: value

profiles:
  production:
    # your config here
```

## Environment
- Python version: [e.g. 3.10.0]
- profile-config version: [e.g. 1.1.0]
- Operating System: [e.g. Ubuntu 22.04, Windows 11, macOS 13.0]
- Configuration format: [e.g. YAML, JSON, TOML]

## Error Message
If applicable, paste the full error message and stack trace:

```
Error traceback here
```

## Additional Context
Add any other context about the problem here.
