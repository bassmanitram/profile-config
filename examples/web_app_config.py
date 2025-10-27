#!/usr/bin/env python3
"""
Real-world web application configuration example.

This example demonstrates how to use profile-config for a typical
web application with different deployment environments.
"""

import os
from pathlib import Path
from typing import Dict, Any

from profile_config import ProfileConfigResolver


class WebAppConfig:
    """Web application configuration manager using profile-config."""
    
    def __init__(self, profile: str = None, config_overrides: Dict[str, Any] = None):
        """
        Initialize web application configuration.
        
        Args:
            profile: Configuration profile to use (default: from environment)
            config_overrides: Runtime configuration overrides
        """
        # Determine profile from environment or parameter
        self.profile = profile or os.environ.get("APP_ENV", "development")
        
        # Add environment-based overrides
        overrides = config_overrides or {}
        self._add_environment_overrides(overrides)
        
        # Initialize resolver
        self.resolver = ProfileConfigResolver(
            config_name="webapp",
            profile=self.profile,
            overrides=overrides
        )
        
        # Load configuration
        self._config = self.resolver.resolve()
        
    def _add_environment_overrides(self, overrides: Dict[str, Any]) -> None:
        """Add configuration overrides from environment variables."""
        env_mappings = {
            "DATABASE_URL": "database.url",
            "REDIS_URL": "cache.redis_url", 
            "SECRET_KEY": "security.secret_key",
            "DEBUG": "debug",
            "PORT": "server.port",
            "LOG_LEVEL": "logging.level",
        }
        
        for env_var, config_key in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                
                # Convert boolean strings
                if value.lower() in ("true", "false"):
                    value = value.lower() == "true"
                # Convert numeric strings
                elif value.isdigit():
                    value = int(value)
                    
                # Set nested configuration
                keys = config_key.split(".")
                current = overrides
                for key in keys[:-1]:
                    current = current.setdefault(key, {})
                current[keys[-1]] = value
    
    @property
    def database_url(self) -> str:
        """Get database connection URL."""
        db_config = self._config.get("database", {})
        return db_config.get("url", "sqlite:///app.db")
    
    @property
    def redis_url(self) -> str:
        """Get Redis connection URL."""
        cache_config = self._config.get("cache", {})
        return cache_config.get("redis_url", "redis://localhost:6379/0")
    
    @property
    def secret_key(self) -> str:
        """Get application secret key."""
        security_config = self._config.get("security", {})
        return security_config.get("secret_key", "dev-secret-key")
    
    @property
    def debug(self) -> bool:
        """Get debug mode setting."""
        return self._config.get("debug", False)
    
    @property
    def server_config(self) -> Dict[str, Any]:
        """Get server configuration."""
        return self._config.get("server", {})
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self._config.get("logging", {})
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self._config.get(key, default)
    
    def get_nested(self, key_path: str, default: Any = None) -> Any:
        """Get nested configuration value by dot-separated path."""
        keys = key_path.split(".")
        current = self._config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
                
        return current


def create_webapp_config():
    """Create a comprehensive web application configuration."""
    config_content = """
# Default configuration
defaults:
  debug: false
  
  # Server settings
  server:
    host: 0.0.0.0
    port: 8000
    workers: 1
    
  # Database settings
  database:
    url: "sqlite:///app.db"
    pool_size: 5
    echo: false
    
  # Cache settings
  cache:
    enabled: true
    redis_url: "redis://localhost:6379/0"
    default_timeout: 300
    
  # Security settings
  security:
    secret_key: change-me-in-production
    session_timeout: 3600
    csrf_enabled: true
    
  # Logging settings
  logging:
    level: INFO
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
  # Feature flags
  features:
    user_registration: true
    email_verification: false
    social_login: false

# Profile configurations
profiles:
  # Base profile with common settings
  base:
    server:
      host: 0.0.0.0
      port: 8000
      workers: 1
    database:
      pool_size: 5
      echo: false
    cache:
      enabled: true
      default_timeout: 300
    security:
      session_timeout: 3600
      csrf_enabled: true
    logging:
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    features:
      user_registration: true
      email_verification: false
      social_login: false

  # Development profile
  development:
    inherits: base
    debug: true
    
    server:
      port: 5000
      workers: 1
      
    database:
      url: "sqlite:///dev.db"
      echo: true
      
    logging:
      level: DEBUG
      
    features:
      email_verification: true
      
  # Testing profile
  testing:
    inherits: development
    
    database:
      url: "sqlite:///:memory:"
      
    cache:
      enabled: false
      
    security:
      secret_key: test-secret-key
      
  # Staging profile
  staging:
    inherits: base
    
    server:
      port: 8080
      workers: 2
      
    database:
      url: "postgresql://user:pass@staging-db:5432/webapp_staging"
      pool_size: 10
      
    cache:
      redis_url: "redis://staging-redis:6379/0"
      
    logging:
      level: INFO
      
    features:
      email_verification: true
      social_login: true
      
  # Production profile
  production:
    inherits: base
    
    server:
      port: 8000
      workers: 4
      
    database:
      url: "postgresql://user:pass@prod-db:5432/webapp_prod"
      pool_size: 20
      
    cache:
      redis_url: "redis://prod-redis:6379/0"
      default_timeout: 600
      
    security:
      session_timeout: 7200
      
    logging:
      level: WARNING
      
    features:
      user_registration: true
      email_verification: true
      social_login: true
"""
    
    # Create config directory and file
    config_dir = Path("webapp")
    config_dir.mkdir(exist_ok=True)
    config_file = config_dir / "config.yaml"
    config_file.write_text(config_content)
    
    return config_file


def demonstrate_webapp_config():
    """Demonstrate web application configuration usage."""
    print("=== Web Application Configuration Example ===\n")
    
    config_file = create_webapp_config()
    
    try:
        # Example 1: Development configuration
        print("1. Development Environment:")
        dev_config = WebAppConfig(profile="development")
        
        print(f"   Debug mode: {dev_config.debug}")
        print(f"   Database URL: {dev_config.database_url}")
        print(f"   Server config: {dev_config.server_config}")
        print(f"   Log level: {dev_config.get_nested('logging.level')}")
        print()
        
        # Example 2: Production configuration
        print("2. Production Environment:")
        prod_config = WebAppConfig(profile="production")
        
        print(f"   Debug mode: {prod_config.debug}")
        print(f"   Database URL: {prod_config.database_url}")
        print(f"   Server workers: {prod_config.get_nested('server.workers')}")
        print(f"   Cache timeout: {prod_config.get_nested('cache.default_timeout')}")
        print()
        
        # Example 3: Environment variable overrides
        print("3. Environment Variable Overrides:")
        
        # Simulate environment variables
        os.environ["DATABASE_URL"] = "postgresql://override:pass@localhost/override_db"
        os.environ["DEBUG"] = "true"
        os.environ["PORT"] = "9000"
        
        override_config = WebAppConfig(profile="production")
        
        print(f"   Database URL (overridden): {override_config.database_url}")
        print(f"   Debug mode (overridden): {override_config.debug}")
        print(f"   Server port (overridden): {override_config.get_nested('server.port')}")
        print()
        
        # Clean up environment
        for key in ["DATABASE_URL", "DEBUG", "PORT"]:
            os.environ.pop(key, None)
        
        # Example 4: Runtime overrides
        print("4. Runtime Configuration Overrides:")
        
        runtime_overrides = {
            "server": {"host": "127.0.0.1", "port": 3000},
            "features": {"social_login": False},
            "custom_setting": "runtime_value"
        }
        
        custom_config = WebAppConfig(
            profile="development", 
            config_overrides=runtime_overrides
        )
        
        print(f"   Server host: {custom_config.get_nested('server.host')}")
        print(f"   Server port: {custom_config.get_nested('server.port')}")
        print(f"   Social login: {custom_config.get_nested('features.social_login')}")
        print(f"   Custom setting: {custom_config.get('custom_setting')}")
        print()
        
    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


def demonstrate_config_validation():
    """Demonstrate configuration validation patterns."""
    print("=== Configuration Validation Example ===\n")
    
    config_file = create_webapp_config()
    
    try:
        def validate_config(config: WebAppConfig) -> None:
            """Validate web application configuration."""
            errors = []
            
            # Validate required settings
            if not config.secret_key or config.secret_key == "change-me-in-production":
                if config.profile == "production":
                    errors.append("Production secret key must be set")
            
            # Validate database URL
            if not config.database_url:
                errors.append("Database URL is required")
            
            # Validate server settings
            port = config.get_nested("server.port")
            if not isinstance(port, int) or port < 1 or port > 65535:
                errors.append(f"Invalid server port: {port}")
            
            # Validate workers for production
            if config.profile == "production":
                workers = config.get_nested("server.workers", 1)
                if workers < 2:
                    errors.append("Production should use at least 2 workers")
            
            if errors:
                raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
        
        # Test validation
        print("Testing configuration validation:")
        
        # Valid development config
        try:
            dev_config = WebAppConfig(profile="development")
            validate_config(dev_config)
            print("   Development config: VALID")
        except ValueError as e:
            print(f"   Development config: INVALID - {e}")
        
        # Invalid production config (default secret key)
        try:
            prod_config = WebAppConfig(profile="production")
            validate_config(prod_config)
            print("   Production config: VALID")
        except ValueError as e:
            print(f"   Production config: INVALID - {e}")
        
        # Fixed production config
        try:
            prod_config = WebAppConfig(
                profile="production",
                config_overrides={"security": {"secret_key": "secure-production-key"}}
            )
            validate_config(prod_config)
            print("   Production config (fixed): VALID")
        except ValueError as e:
            print(f"   Production config (fixed): INVALID - {e}")
        
        print()
        
    finally:
        # Cleanup
        config_file.unlink()
        config_file.parent.rmdir()


if __name__ == "__main__":
    demonstrate_webapp_config()
    demonstrate_config_validation()