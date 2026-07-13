"""
Unit tests for SOLO ROCK HardwareReader.
"""

import pytest
import os
import sys
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hardware_drivers.hardware_reader import HardwareReader


class TestHardwareReaderTelemetry:
    """Test telemetry snapshot collection."""

    def test_get_telemetry_snapshot_with_mocks(self, mock_psutil):
        """Test getting telemetry snapshot with mocked psutil."""
        reader = HardwareReader()

        # Get snapshot
        snapshot = reader.get_telemetry_snapshot()

        # Verify structure
        assert isinstance(snapshot, dict)
        assert 'cpu_load' in snapshot
        assert 'cpu_temp' in snapshot
        assert 'ram_usage' in snapshot

        # Verify values from mocks
        assert snapshot['cpu_load'] == 50.0
        assert snapshot['cpu_temp'] == 65.0
        assert snapshot['ram_usage'] == 60.0

    def test_get_telemetry_snapshot_structure(self, mock_psutil):
        """Test telemetry snapshot has expected structure."""
        reader = HardwareReader()
        snapshot = reader.get_telemetry_snapshot()

        # Required fields
        required_fields = ['cpu_load', 'cpu_temp', 'ram_usage']
        for field in required_fields:
            assert field in snapshot
            assert isinstance(snapshot[field], (int, float))
            assert snapshot[field] >= 0

    def test_telemetry_values_in_valid_range(self, mock_psutil):
        """Test that telemetry values are in expected ranges."""
        reader = HardwareReader()
        snapshot = reader.get_telemetry_snapshot()

        # CPU load should be 0-100%
        assert 0 <= snapshot['cpu_load'] <= 100

        # RAM usage should be 0-100%
        assert 0 <= snapshot['ram_usage'] <= 100

        # Temperature should be reasonable (0-150C)
        assert 0 <= snapshot['cpu_temp'] <= 150


class TestHardwareReaderGracefulDegradation:
    """Test graceful fallback when sensors unavailable."""

    def test_cpu_temp_unavailable(self):
        """Test behavior when CPU temperature sensor unavailable."""
        with patch('psutil.sensors_temperatures') as mock_temps:
            mock_temps.return_value = {}  # No temperature data

            reader = HardwareReader()
            snapshot = reader.get_telemetry_snapshot()

            # Should still have cpu_temp key but with default or None
            assert 'cpu_temp' in snapshot or snapshot.get('cpu_temp') == 0.0

    def test_psutil_unavailable(self):
        """Test behavior when psutil functions fail."""
        with patch('psutil.cpu_percent') as mock_cpu:
            mock_cpu.side_effect = Exception("psutil not available")

            reader = HardwareReader()
            snapshot = reader.get_telemetry_snapshot()

            # Should still return a snapshot dict (even if with default values)
            assert isinstance(snapshot, dict)
            assert 'cpu_load' in snapshot

    def test_memory_unavailable(self):
        """Test behavior when memory sensor unavailable."""
        with patch('psutil.virtual_memory') as mock_mem:
            mock_mem.side_effect = Exception("Memory info unavailable")

            reader = HardwareReader()
            snapshot = reader.get_telemetry_snapshot()

            # Should still have ram_usage key
            assert isinstance(snapshot, dict)
            assert 'ram_usage' in snapshot


class TestHardwareReaderCPUReading:
    """Test CPU-specific readings."""

    def test_cpu_load_percentage(self, mock_psutil):
        """Test CPU load is returned as percentage."""
        reader = HardwareReader()
        snapshot = reader.get_telemetry_snapshot()

        cpu_load = snapshot['cpu_load']
        assert isinstance(cpu_load, (int, float))
        assert 0 <= cpu_load <= 100

    def test_cpu_temperature_celsius(self, mock_psutil):
        """Test CPU temperature is returned in Celsius."""
        reader = HardwareReader()
        snapshot = reader.get_telemetry_snapshot()

        cpu_temp = snapshot['cpu_temp']
        assert isinstance(cpu_temp, (int, float))
        # Reasonable range: -10 to 150°C
        assert -10 <= cpu_temp <= 150


class TestHardwareReaderRAMReading:
    """Test RAM-specific readings."""

    def test_ram_usage_percentage(self, mock_psutil):
        """Test RAM usage is returned as percentage."""
        reader = HardwareReader()
        snapshot = reader.get_telemetry_snapshot()

        ram_usage = snapshot['ram_usage']
        assert isinstance(ram_usage, (int, float))
        assert 0 <= ram_usage <= 100


class TestHardwareReaderMultipleSnapshots:
    """Test multiple consecutive snapshot readings."""

    def test_consistent_snapshot_structure(self, mock_psutil):
        """Test that multiple snapshots have consistent structure."""
        reader = HardwareReader()

        for _ in range(5):
            snapshot = reader.get_telemetry_snapshot()
            assert 'cpu_load' in snapshot
            assert 'cpu_temp' in snapshot
            assert 'ram_usage' in snapshot


class TestHardwareReaderEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_values(self, mock_psutil):
        """Test handling of zero sensor values."""
        with patch('psutil.cpu_percent') as mock_cpu:
            mock_cpu.return_value = 0.0

            reader = HardwareReader()
            snapshot = reader.get_telemetry_snapshot()

            assert snapshot['cpu_load'] == 0.0

    def test_max_values(self, mock_psutil):
        """Test handling of maximum sensor values."""
        with patch('psutil.cpu_percent') as mock_cpu:
            mock_cpu.return_value = 100.0

            reader = HardwareReader()
            snapshot = reader.get_telemetry_snapshot()

            assert snapshot['cpu_load'] == 100.0

    def test_repeated_reads_no_crash(self, mock_psutil):
        """Test that repeated reads don't cause issues."""
        reader = HardwareReader()

        try:
            for _ in range(100):
                snapshot = reader.get_telemetry_snapshot()
                assert isinstance(snapshot, dict)
        except Exception as e:
            pytest.fail(f"Repeated reads caused crash: {e}")


class TestHardwareReaderCrossPlatform:
    """Test cross-platform compatibility."""

    def test_snapshot_works_on_different_platforms(self, mock_psutil):
        """Test that snapshot collection works regardless of platform."""
        reader = HardwareReader()

        # Should work on any platform (psutil is mocked)
        snapshot = reader.get_telemetry_snapshot()
        assert isinstance(snapshot, dict)
        assert len(snapshot) > 0

    def test_graceful_fallback_different_os(self):
        """Test graceful fallback on different OS."""
        # Test with mocked failures
        with patch('psutil.sensors_temperatures') as mock_temps:
            # Simulate OSError (e.g., permission denied on Linux)
            mock_temps.side_effect = OSError("Permission denied")

            reader = HardwareReader()
            snapshot = reader.get_telemetry_snapshot()

            # Should still return valid snapshot
            assert isinstance(snapshot, dict)
            assert 'cpu_load' in snapshot
            assert 'ram_usage' in snapshot


class TestHardwareReaderNumericalStability:
    """Test numerical stability of readings."""

    def test_float_precision_preserved(self, mock_psutil):
        """Test that float precision is preserved."""
        reader = HardwareReader()
        snapshot = reader.get_telemetry_snapshot()

        # Values should be floats with reasonable precision
        for key in ['cpu_load', 'cpu_temp', 'ram_usage']:
            value = snapshot[key]
            assert isinstance(value, (int, float))
            # Should not be NaN or Inf
            assert value == value  # NaN != NaN
            assert abs(value) != float('inf')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
