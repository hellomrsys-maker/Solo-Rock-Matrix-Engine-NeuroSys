"""
Pytest configuration and shared fixtures for SOLO ROCK tests.
"""

import pytest
import os
import tempfile
import json
from unittest.mock import Mock, patch


@pytest.fixture
def mock_telemetry_idle():
    """Mock telemetry snapshot for idle system."""
    return {
        "cpu_temp": 45.0,
        "cpu_load": 10.0,
        "ram_usage": 40.0,
        "gpu_load": 5.0,
    }


@pytest.fixture
def mock_telemetry_moderate():
    """Mock telemetry snapshot for moderate load."""
    return {
        "cpu_temp": 65.0,
        "cpu_load": 60.0,
        "ram_usage": 55.0,
        "gpu_load": 50.0,
    }


@pytest.fixture
def mock_telemetry_high():
    """Mock telemetry snapshot for high load."""
    return {
        "cpu_temp": 85.0,
        "cpu_load": 92.0,
        "ram_usage": 70.0,
        "gpu_load": 95.0,
    }


@pytest.fixture
def mock_telemetry_critical():
    """Mock telemetry snapshot for critical state."""
    return {
        "cpu_temp": 95.0,
        "cpu_load": 99.0,
        "ram_usage": 98.0,
        "gpu_load": 100.0,
    }


@pytest.fixture
def temp_config_file():
    """Create a temporary YAML config file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_content = """
thermal:
  warning_celsius: 75
  critical_celsius: 85
  throttle_threshold: 70
cpu:
  load_high_percent: 80
  load_critical_percent: 95
ram:
  critical_percent: 97
decisions:
  batch_threshold: 4
  throttle_pacing_ms: 50
  emergency_hold_ms: 100
"""
        f.write(config_content)
        f.flush()
        yield f.name

    # Cleanup
    if os.path.exists(f.name):
        os.unlink(f.name)


@pytest.fixture
def temp_calibration_file():
    """Create a temporary calibration.json file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        calibration_content = {
            "thermal": {
                "warning_celsius": 72,
                "critical_celsius": 85,
                "throttle_threshold": 70,
            },
            "cpu": {
                "load_high_percent": 78,
                "load_critical_percent": 95,
            },
            "ram": {
                "critical_percent": 97,
            },
            "decisions": {
                "batch_threshold": 4,
                "throttle_pacing_ms": 50,
                "emergency_hold_ms": 100,
            }
        }
        json.dump(calibration_content, f)
        f.flush()
        yield f.name

    # Cleanup
    if os.path.exists(f.name):
        os.unlink(f.name)


@pytest.fixture
def mock_psutil():
    """Mock psutil functions for testing hardware reader."""
    with patch('psutil.cpu_percent') as mock_cpu, \
         patch('psutil.virtual_memory') as mock_memory, \
         patch('psutil.sensors_temperatures') as mock_temps:

        mock_cpu.return_value = 50.0
        mock_memory.return_value = Mock(percent=60.0)
        mock_temps.return_value = {'coretemp': [Mock(current=65.0)]}

        yield {
            'cpu': mock_cpu,
            'memory': mock_memory,
            'temps': mock_temps,
        }


@pytest.fixture(autouse=True)
def cleanup_calibration():
    """Cleanup calibration.json before and after each test to prevent test interference."""
    # Cleanup before
    calibration_path = os.path.join(
        os.path.dirname(__file__),
        '../config/calibration.json'
    )
    if os.path.exists(calibration_path):
        try:
            os.unlink(calibration_path)
        except:
            pass

    yield

    # Cleanup after
    if os.path.exists(calibration_path):
        try:
            os.unlink(calibration_path)
        except:
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
