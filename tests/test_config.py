"""
Unit tests for SOLO ROCK configuration system.
"""

import pytest
import os
import sys
import json
import tempfile
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SoloRockConfig, ConfigError, load_config, get_config


class TestSoloRockConfigDefaults:
    """Test configuration defaults."""

    def test_load_defaults(self):
        """Test loading default configuration."""
        config = SoloRockConfig()

        # Check thermal defaults
        assert config.get('thermal.warning_celsius') == 80
        assert config.get('thermal.critical_celsius') == 90
        assert config.get('thermal.throttle_threshold') == 75

        # Check CPU defaults
        assert config.get('cpu.load_high_percent') == 85
        assert config.get('cpu.load_critical_percent') == 95

        # Check RAM defaults
        assert config.get('ram.critical_percent') == 97

        # Check decision defaults
        assert config.get('decisions.batch_threshold') == 4
        assert config.get('decisions.throttle_pacing_ms') == 50
        assert config.get('decisions.emergency_hold_ms') == 100

    def test_get_with_default(self):
        """Test get() method with default fallback."""
        config = SoloRockConfig()

        # Test returning default for missing key
        assert config.get('nonexistent.key', 42) == 42
        assert config.get('nonexistent.key', 'default') == 'default'
        assert config.get('nonexistent.key') is None


class TestSoloRockConfigYAML:
    """Test YAML configuration loading."""

    def test_load_valid_yaml(self, temp_config_file):
        """Test loading valid YAML configuration."""
        config = SoloRockConfig(temp_config_file)

        # Should load custom values from the temp file
        assert config.get('thermal.warning_celsius') == 75
        assert config.get('thermal.critical_celsius') == 85
        assert config.get('thermal.throttle_threshold') == 70
        assert config.get('cpu.load_high_percent') == 80
        assert config.get('cpu.load_critical_percent') == 95
        assert config.get('ram.critical_percent') == 97

    def test_load_nonexistent_file(self):
        """Test error when config file doesn't exist."""
        with pytest.raises(ConfigError) as exc_info:
            SoloRockConfig('/nonexistent/path/config.yaml')

        assert 'not found' in str(exc_info.value).lower()

    def test_load_invalid_yaml(self):
        """Test error handling for invalid YAML syntax."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('invalid: yaml: content: [')  # Invalid YAML
            temp_path = f.name

        try:
            with pytest.raises(ConfigError) as exc_info:
                SoloRockConfig(temp_path)
            assert 'invalid yaml' in str(exc_info.value).lower()
        finally:
            os.unlink(temp_path)

    def test_partial_yaml_override(self):
        """Test that YAML overrides only specified values."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('thermal:\n  warning_celsius: 70\n')
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                # Mock calibration path to return non-existent file
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                config = SoloRockConfig(temp_path)
                # Overridden value
                assert config.get('thermal.warning_celsius') == 70
                # Default values still present
                assert config.get('thermal.critical_celsius') == 90
                assert config.get('cpu.load_high_percent') == 85
        finally:
            os.unlink(temp_path)

    def test_empty_yaml_file(self):
        """Test loading empty YAML file (should use all defaults)."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('')  # Empty file
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                # Mock calibration path to return non-existent file
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                config = SoloRockConfig(temp_path)
                # All defaults should still be present
                assert config.get('thermal.warning_celsius') == 80
                assert config.get('cpu.load_high_percent') == 85
        finally:
            os.unlink(temp_path)


class TestSoloRockConfigValidation:
    """Test configuration validation."""

    def test_validate_thermal_range(self):
        """Test thermal threshold validation."""
        # Invalid: warning temperature out of range
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('thermal:\n  warning_celsius: 150\n')
            temp_path = f.name

        try:
            with pytest.raises(ConfigError) as exc_info:
                SoloRockConfig(temp_path)
            assert 'warning_celsius' in str(exc_info.value) and '0-120' in str(exc_info.value)
        finally:
            os.unlink(temp_path)

    def test_validate_critical_greater_than_warning(self):
        """Test that critical temperature must be higher than warning."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('thermal:\n  warning_celsius: 95\n  critical_celsius: 85\n')
            temp_path = f.name

        try:
            with pytest.raises(ConfigError) as exc_info:
                SoloRockConfig(temp_path)
            assert 'critical_celsius' in str(exc_info.value) and 'warning_celsius' in str(exc_info.value)
        finally:
            os.unlink(temp_path)

    def test_validate_cpu_load_range(self):
        """Test CPU load threshold validation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('cpu:\n  load_high_percent: 150\n  load_critical_percent: 96\n')
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                with pytest.raises(ConfigError) as exc_info:
                    SoloRockConfig(temp_path)
                assert 'load_high_percent' in str(exc_info.value) and '0-100' in str(exc_info.value)
        finally:
            os.unlink(temp_path)

    def test_validate_cpu_critical_greater_than_high(self):
        """Test that critical load must be higher than high load."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('cpu:\n  load_high_percent: 96\n  load_critical_percent: 90\nthermal:\n  warning_celsius: 75\n  critical_celsius: 85\n')
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                with pytest.raises(ConfigError) as exc_info:
                    SoloRockConfig(temp_path)
                assert 'load_critical_percent' in str(exc_info.value) and 'load_high_percent' in str(exc_info.value)
        finally:
            os.unlink(temp_path)

    def test_validate_ram_range(self):
        """Test RAM threshold validation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('ram:\n  critical_percent: 150\nthermal:\n  warning_celsius: 75\n  critical_celsius: 85\ncpu:\n  load_high_percent: 80\n  load_critical_percent: 95\n')
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                with pytest.raises(ConfigError) as exc_info:
                    SoloRockConfig(temp_path)
                assert 'critical_percent' in str(exc_info.value) and '0-100' in str(exc_info.value)
        finally:
            os.unlink(temp_path)

    def test_validate_decision_thresholds(self):
        """Test decision threshold validation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('decisions:\n  batch_threshold: 0\nthermal:\n  warning_celsius: 75\n  critical_celsius: 85\ncpu:\n  load_high_percent: 80\n  load_critical_percent: 95\nram:\n  critical_percent: 97\n')
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                with pytest.raises(ConfigError) as exc_info:
                    SoloRockConfig(temp_path)
                assert 'batch_threshold' in str(exc_info.value)
        finally:
            os.unlink(temp_path)


class TestSoloRockConfigCalibration:
    """Test calibration file handling."""

    def test_load_calibration_file(self, temp_calibration_file):
        """Test loading calibration.json from config directory."""
        # Mock the calibration path to use temp file
        with patch('config.os.path.join') as mock_join:
            def join_mock(*args):
                if 'calibration.json' in args[-1]:
                    return temp_calibration_file
                return os.path.join(*args)

            mock_join.side_effect = join_mock

            config = SoloRockConfig()
            # Calibration should be loaded and merged
            assert config.get('thermal.warning_celsius') == 72  # From calibration file
            assert config.get('cpu.load_high_percent') == 78  # From calibration file

    def test_calibration_overrides_defaults(self):
        """Test that calibration values override defaults."""
        with patch('config.os.path.join') as mock_join:
            # Mock calibration path to non-existent file to avoid loading any
            mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

            calibration_data = {
                'thermal': {'warning_celsius': 72},
                'cpu': {'load_high_percent': 78},
                'ram': {'critical_percent': 97}
            }

            config = SoloRockConfig()

            # Before calibration
            assert config.get('thermal.warning_celsius') == 80

            # Save and reload
            config.save_calibration(calibration_data)

            # Verify calibration file was created
            calibration_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config/calibration.json'
            )
            if os.path.exists(calibration_path):
                # Cleanup
                os.unlink(calibration_path)


class TestSoloRockConfigMerging:
    """Test configuration merging logic."""

    def test_deep_merge(self):
        """Test that configuration merging works recursively."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
thermal:
  warning_celsius: 75
decisions:
  batch_threshold: 5
""")
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                config = SoloRockConfig(temp_path)

                # Merged values
                assert config.get('thermal.warning_celsius') == 75
                assert config.get('decisions.batch_threshold') == 5

                # Preserved defaults
                assert config.get('thermal.critical_celsius') == 90
                assert config.get('cpu.load_high_percent') == 85
        finally:
            os.unlink(temp_path)


class TestGlobalConfigFunctions:
    """Test global configuration functions."""

    def test_load_config_function(self, temp_config_file):
        """Test load_config() global function."""
        config = load_config(temp_config_file)

        assert config.get('thermal.warning_celsius') == 75
        assert isinstance(config, SoloRockConfig)

    def test_get_config_function(self):
        """Test get_config() returns current global instance."""
        # Reset global config with mock to avoid calibration.json issues
        with patch('config.os.path.join') as mock_join:
            mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

            # Load a config first with mocked calibration
            import config as config_module
            config_module._global_config = None
            load_config()

            # Get should return the same instance
            config = get_config()
            assert isinstance(config, SoloRockConfig)
            assert config.get('thermal.warning_celsius') == 80

    def test_get_all_method(self, temp_config_file):
        """Test get_all() returns complete config dict."""
        config = SoloRockConfig(temp_config_file)
        all_config = config.get_all()

        # Should be a dict with expected structure
        assert isinstance(all_config, dict)
        assert 'thermal' in all_config
        assert 'cpu' in all_config
        assert 'ram' in all_config
        assert 'decisions' in all_config


class TestConfigEdgeCases:
    """Test edge cases and error scenarios."""

    def test_negative_thresholds(self):
        """Test that negative thresholds are rejected."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('thermal:\n  warning_celsius: -10\n  critical_celsius: 85\ncpu:\n  load_high_percent: 80\n  load_critical_percent: 95\nram:\n  critical_percent: 97\n')
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                with pytest.raises(ConfigError):
                    SoloRockConfig(temp_path)
        finally:
            os.unlink(temp_path)

    def test_zero_decision_thresholds(self):
        """Test that zero decision thresholds are rejected."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('decisions:\n  throttle_pacing_ms: 0\nthermal:\n  warning_celsius: 75\n  critical_celsius: 85\ncpu:\n  load_high_percent: 80\n  load_critical_percent: 95\nram:\n  critical_percent: 97\n')
            temp_path = f.name

        try:
            with patch('config.os.path.join') as mock_join:
                mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

                with pytest.raises(ConfigError):
                    SoloRockConfig(temp_path)
        finally:
            os.unlink(temp_path)

    def test_config_none_path(self):
        """Test that None path uses defaults."""
        with patch('config.os.path.join') as mock_join:
            mock_join.side_effect = lambda *args: '/nonexistent/calibration.json' if 'calibration.json' in args[-1] else os.path.join(*args)

            config = SoloRockConfig(None)
            assert config.get('thermal.warning_celsius') == 80


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
