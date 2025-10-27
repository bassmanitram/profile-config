"""
Profile Config - Hierarchical profile-based configuration management.

This package provides configuration resolution with:
- Hierarchical directory discovery
- Profile inheritance
- Configurable search patterns
- Multiple file format support
"""

from .resolver import ProfileConfigResolver
from .discovery import ConfigDiscovery
from .profiles import ProfileResolver
from .merger import ConfigMerger
from .exceptions import (
    ProfileConfigError,
    ConfigNotFoundError,
    ProfileNotFoundError,
    CircularInheritanceError,
)

__version__ = "1.0.1"
__all__ = [
    "ProfileConfigResolver",
    "ConfigDiscovery", 
    "ProfileResolver",
    "ConfigMerger",
    "ProfileConfigError",
    "ConfigNotFoundError",
    "ProfileNotFoundError",
    "CircularInheritanceError",
]