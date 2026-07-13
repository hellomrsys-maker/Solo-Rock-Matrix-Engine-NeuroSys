"""
Unit tests for SOLO ROCK DecisionEngine.
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from central_command.decision_engine import (
    DecisionEngine, FULL_RATE, BATCH, THROTTLE, EMERGENCY
)
from config import SoloRockConfig


class TestDecisionEngineDefaults:
    """Test DecisionEngine with default thresholds."""

    def test_full_rate_idle_load(self):
        """Test FULL_RATE decision on idle system."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 45.0,
            'cpu_load': 10.0,
            'ram_usage': 40.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == FULL_RATE
        assert 'headroom' in reason.lower()

    def test_batch_moderate_load(self):
        """Test BATCH decision on moderate load."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 65.0,
            'cpu_load': 60.0,
            'ram_usage': 55.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == BATCH
        assert 'moderate' in reason.lower()

    def test_throttle_high_load(self):
        """Test THROTTLE decision on high CPU/thermal load."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 85.0,
            'cpu_load': 92.0,
            'ram_usage': 70.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == THROTTLE

    def test_emergency_thermal_critical(self):
        """Test EMERGENCY decision on critical temperature."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 95.0,  # >= 90.0 critical
            'cpu_load': 50.0,
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == EMERGENCY
        assert 'critical' in reason.lower()

    def test_emergency_ram_critical(self):
        """Test EMERGENCY decision on critical RAM usage."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 50.0,
            'ram_usage': 98.0,  # >= 97.0 critical
        }

        action, reason = engine.decide(snapshot)

        assert action == EMERGENCY
        assert 'ram' in reason.lower()


class TestDecisionEngineBoundaryConditions:
    """Test decision engine at threshold boundaries."""

    def test_just_below_thermal_warning(self):
        """Test just below thermal warning threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 79.9,  # < 80.0 warning
            'cpu_load': 90.0,
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        # With high load but temp below warning: should be BATCH
        assert action == BATCH

    def test_at_thermal_warning(self):
        """Test at exact thermal warning threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 80.0,  # Exactly at warning
            'cpu_load': 30.0,
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        # At thermal warning: should trigger THROTTLE
        assert action == THROTTLE

    def test_just_below_cpu_load_moderate(self):
        """Test just below moderate CPU load threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 49.9,  # < 50.0 moderate
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == FULL_RATE

    def test_at_cpu_load_moderate(self):
        """Test at exact moderate CPU load threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 50.0,  # Exactly at moderate
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == BATCH

    def test_just_below_cpu_load_high(self):
        """Test just below high CPU load threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 84.9,  # < 85.0 high
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == BATCH

    def test_at_cpu_load_high(self):
        """Test at exact high CPU load threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 85.0,  # Exactly at high
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        # At CPU load high: should trigger THROTTLE
        assert action == THROTTLE

    def test_at_thermal_critical(self):
        """Test at exact thermal critical threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 90.0,  # Exactly at critical
            'cpu_load': 50.0,
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        assert action == EMERGENCY

    def test_at_ram_critical(self):
        """Test at exact RAM critical threshold."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 50.0,
            'ram_usage': 97.0,  # Exactly at critical
        }

        action, reason = engine.decide(snapshot)

        assert action == EMERGENCY


class TestDecisionEngineWithConfig:
    """Test DecisionEngine with custom configuration."""

    def test_custom_thermal_thresholds(self, temp_config_file):
        """Test that DecisionEngine respects custom thermal thresholds."""
        config = SoloRockConfig(temp_config_file)
        # temp_config_file has: warning=75, critical=85

        engine = DecisionEngine(config=config)

        # At 76°C (above custom warning of 75):
        snapshot = {
            'cpu_temp': 76.0,
            'cpu_load': 30.0,
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)
        assert action == THROTTLE  # Should throttle at custom warning

    def test_custom_cpu_load_thresholds(self, temp_config_file):
        """Test that DecisionEngine respects custom CPU load thresholds."""
        config = SoloRockConfig(temp_config_file)
        # temp_config_file has: load_high_percent=80

        engine = DecisionEngine(config=config)

        # At 81% load (above custom high of 80):
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 81.0,
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)
        assert action == THROTTLE  # Should throttle at custom high load

    def test_custom_ram_threshold(self, temp_config_file):
        """Test that DecisionEngine respects custom RAM thresholds."""
        config = SoloRockConfig(temp_config_file)
        # temp_config_file has: critical_percent=97 (same as default)

        engine = DecisionEngine(config=config)

        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 50.0,
            'ram_usage': 97.0,
        }

        action, reason = engine.decide(snapshot)
        assert action == EMERGENCY


class TestDecisionEngineClassifyWorkload:
    """Test workload classification."""

    def test_classify_idle(self):
        """Test IDLE classification."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 40.0,
            'cpu_load': 3.0,
            'ram_usage': 30.0,
        }

        workload = engine.classify_workload(snapshot)
        assert workload == 'IDLE'

    def test_classify_light(self):
        """Test LIGHT classification."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            'cpu_load': 15.0,
            'ram_usage': 40.0,
        }

        workload = engine.classify_workload(snapshot)
        assert workload == 'LIGHT'

    def test_classify_moderate(self):
        """Test MODERATE classification."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 60.0,
            'cpu_load': 60.0,
            'ram_usage': 50.0,
        }

        workload = engine.classify_workload(snapshot)
        assert workload == 'MODERATE'

    def test_classify_heavy(self):
        """Test HEAVY classification."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 75.0,
            'cpu_load': 86.0,
            'ram_usage': 70.0,
        }

        workload = engine.classify_workload(snapshot)
        assert workload == 'HEAVY'

    def test_classify_critical_by_temperature(self):
        """Test CRITICAL classification by temperature."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 91.0,  # > critical (90)
            'cpu_load': 50.0,
            'ram_usage': 50.0,
        }

        workload = engine.classify_workload(snapshot)
        assert workload == 'CRITICAL'


class TestDecisionEngineEdgeCases:
    """Test edge cases."""

    def test_missing_telemetry_values(self):
        """Test handling of missing telemetry values."""
        engine = DecisionEngine()
        snapshot = {}  # All values missing

        action, reason = engine.decide(snapshot)

        # With all values at 0, should be FULL_RATE
        assert action == FULL_RATE

    def test_partial_telemetry_values(self):
        """Test handling of partially missing telemetry values."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 50.0,
            # cpu_load missing
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)

        # cpu_load defaults to 0.0, rest are values
        assert action in [FULL_RATE, BATCH, THROTTLE, EMERGENCY]

    def test_extreme_high_values(self):
        """Test handling of extreme high values."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 200.0,  # Way above critical
            'cpu_load': 150.0,  # Above 100%
            'ram_usage': 200.0,  # Above 100%
        }

        action, reason = engine.decide(snapshot)

        # Should trigger EMERGENCY (temperature alone is > critical)
        assert action == EMERGENCY

    def test_negative_values(self):
        """Test handling of negative values (shouldn't happen but should not crash)."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': -10.0,
            'cpu_load': -5.0,
            'ram_usage': -10.0,
        }

        action, reason = engine.decide(snapshot)

        # Negative values: all comparisons will be false → FULL_RATE
        assert action == FULL_RATE


class TestDecisionEnginePriority:
    """Test decision priority (critical > warning > moderate > full rate)."""

    def test_emergency_takes_priority_over_throttle(self):
        """Test that EMERGENCY takes priority over THROTTLE."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 91.0,  # Triggers EMERGENCY (> 90)
            'cpu_load': 90.0,  # Also high (would trigger THROTTLE)
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)
        assert action == EMERGENCY

    def test_throttle_takes_priority_over_batch(self):
        """Test that THROTTLE takes priority over BATCH."""
        engine = DecisionEngine()
        snapshot = {
            'cpu_temp': 80.0,  # At warning (triggers THROTTLE)
            'cpu_load': 60.0,  # Moderate (would trigger BATCH)
            'ram_usage': 50.0,
        }

        action, reason = engine.decide(snapshot)
        assert action == THROTTLE


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
