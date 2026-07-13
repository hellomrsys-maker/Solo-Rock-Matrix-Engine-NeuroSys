"""
Configuration Loader for SOLO ROCK

Loads YAML configuration files and provides validated thresholds
to the Decision Engine and other components.
"""

import os
import sys
import json
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import yaml
except ImportError:
    yaml = None


class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass


class SoloRockConfig:
    """Configuration manager for SOLO ROCK thresholds."""

    # Default thresholds (hardcoded fallback)
    DEFAULTS = {
        'thermal': {
            'warning_celsius': 80,
            'critical_celsius': 90,
            'throttle_threshold': 75,
        },
        'cpu': {
            'load_high_percent': 85,
            'load_critical_percent': 95,
        },
        'ram': {
            'critical_percent': 97,
        },
        'decisions': {
            'batch_threshold': 4,
            'throttle_pacing_ms': 50,
            'emergency_hold_ms': 100,
        }
    }

    def __init__(self, config_path=None):
        """
        Initialize configuration.

        Args:
            config_path (str): Path to YAML config file. If None, use defaults.
        """
        self.config_path = config_path
        self.config = self.DEFAULTS.copy()
        self.calibration = {}

        if config_path:
            self._load_yaml_config(config_path)

        # Try to load calibration (auto-tuned values)
        self._load_calibration()

        # Validate after loading
        self._validate()

    def _load_yaml_config(self, path):
        """Load configuration from YAML file."""
        if not yaml:
            raise ConfigError(
                "PyYAML not installed. Install with: pip install pyyaml"
            )

        if not os.path.exists(path):
            raise ConfigError(f"Config file not found: {path}")

        try:
            with open(path, 'r') as f:
                user_config = yaml.safe_load(f) or {}

            # Recursively merge user config with defaults
            self._merge_config(self.config, user_config)

        except yaml.YAMLError as e:
            raise ConfigError(f"Invalid YAML in {path}: {e}")
        except IOError as e:
            raise ConfigError(f"Cannot read {path}: {e}")

    def _merge_config(self, base, override):
        """Recursively merge override config into base config."""
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def _load_calibration(self):
        """Load hardware-specific calibration if available."""
        calibration_path = os.path.join(
            os.path.dirname(__file__),
            'config/calibration.json'
        )

        if not os.path.exists(calibration_path):
            return

        try:
            with open(calibration_path, 'r') as f:
                self.calibration = json.load(f)

            # Merge calibration into config (overrides user config)
            self._merge_config(self.config, self.calibration)

        except (IOError, json.JSONDecodeError) as e:
            # Silently ignore calibration errors
            pass

    def _validate(self):
        """Validate that all thresholds are in safe ranges."""
        thermal = self.config['thermal']
        cpu = self.config['cpu']
        ram = self.config['ram']

        # Temperature validation
        if not 0 <= thermal['warning_celsius'] <= 120:
            raise ConfigError(
                f"thermal.warning_celsius must be 0-120, got {thermal['warning_celsius']}"
            )
        if not 0 <= thermal['critical_celsius'] <= 120:
            raise ConfigError(
                f"thermal.critical_celsius must be 0-120, got {thermal['critical_celsius']}"
            )
        if thermal['critical_celsius'] <= thermal['warning_celsius']:
            raise ConfigError(
                f"critical_celsius ({thermal['critical_celsius']}) must be > "
                f"warning_celsius ({thermal['warning_celsius']})"
            )

        # CPU load validation
        if not 0 <= cpu['load_high_percent'] <= 100:
            raise ConfigError(
                f"cpu.load_high_percent must be 0-100, got {cpu['load_high_percent']}"
            )
        if not 0 <= cpu['load_critical_percent'] <= 100:
            raise ConfigError(
                f"cpu.load_critical_percent must be 0-100, got {cpu['load_critical_percent']}"
            )
        if cpu['load_critical_percent'] <= cpu['load_high_percent']:
            raise ConfigError(
                f"load_critical_percent ({cpu['load_critical_percent']}) must be > "
                f"load_high_percent ({cpu['load_high_percent']})"
            )

        # RAM validation
        if not 0 <= ram['critical_percent'] <= 100:
            raise ConfigError(
                f"ram.critical_percent must be 0-100, got {ram['critical_percent']}"
            )

        # Decision tuning validation
        decisions = self.config['decisions']
        if decisions['batch_threshold'] < 1:
            raise ConfigError(
                f"decisions.batch_threshold must be >= 1, got {decisions['batch_threshold']}"
            )
        if decisions['throttle_pacing_ms'] < 1:
            raise ConfigError(
                f"decisions.throttle_pacing_ms must be >= 1, got {decisions['throttle_pacing_ms']}"
            )
        if decisions['emergency_hold_ms'] < 1:
            raise ConfigError(
                f"decisions.emergency_hold_ms must be >= 1, got {decisions['emergency_hold_ms']}"
            )

    def get(self, key_path, default=None):
        """
        Get configuration value by dot-notation path.

        Example:
            config.get('thermal.warning_celsius')  # → 80
            config.get('unknown.path', 100)         # → 100 (default)
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_all(self):
        """Return entire configuration dict."""
        return self.config.copy()

    def save_calibration(self, calibration_values):
        """
        Save hardware-specific calibration to calibration.json.

        Args:
            calibration_values (dict): Nested dict of tuned thresholds
        """
        calibration_path = os.path.join(
            os.path.dirname(__file__),
            'config/calibration.json'
        )

        try:
            os.makedirs(os.path.dirname(calibration_path), exist_ok=True)
            with open(calibration_path, 'w') as f:
                json.dump(calibration_values, f, indent=2)
        except IOError as e:
            raise ConfigError(f"Cannot write calibration: {e}")


# Global config instance
_global_config = None


def load_config(config_path=None):
    """
    Load and return global config instance.

    Args:
        config_path (str): Path to YAML config file. If None, use defaults.

    Returns:
        SoloRockConfig: Configuration instance
    """
    global _global_config
    _global_config = SoloRockConfig(config_path)
    return _global_config


def get_config():
    """Get the current global config instance."""
    global _global_config
    if _global_config is None:
        _global_config = SoloRockConfig()
    return _global_config


if __name__ == "__main__":
    # Test the configuration loader
    print("Loading default configuration...")
    config = SoloRockConfig()
    print(f"Thermal warning: {config.get('thermal.warning_celsius')}°C")
    print(f"CPU load high: {config.get('cpu.load_high_percent')}%")
    print(f"RAM critical: {config.get('ram.critical_percent')}%")
    print()

    # Test custom configuration
    default_yaml = os.path.join(os.path.dirname(__file__), 'config/thresholds.yaml')
    if os.path.exists(default_yaml):
        print(f"Loading from {default_yaml}...")
        config = SoloRockConfig(default_yaml)
        print(f"Thermal warning: {config.get('thermal.warning_celsius')}°C")
        print(f"All config: {config.get_all()}")
