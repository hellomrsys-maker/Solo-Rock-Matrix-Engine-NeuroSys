"""
Telemetry analysis and trend detection from historical event database.

Provides utilities to analyze performance metrics, detect thermal trends,
and calculate decision distribution statistics from logged events.
"""

import statistics
from datetime import datetime, timedelta
from diagnostics.logger import EventLogger


class TelemetryAnalyzer:
    """Analyzes historical telemetry data from SQLite database."""

    def __init__(self, db_path='solo_rock.db'):
        """Initialize with database path.

        Args:
            db_path: Path to SQLite database file (default: solo_rock.db)
        """
        self.logger = EventLogger(db_path)

    def get_decision_distribution(self, hours=1):
        """Get distribution of decisions in last N hours.

        Args:
            hours: Number of hours to analyze (default: 1)

        Returns:
            Dictionary with counts, percentages, and total_events
        """
        since = datetime.now() - timedelta(hours=hours)
        events = self.logger.get_events_since(since.timestamp())

        distribution = {}
        for event in events:
            decision = event['decision']
            distribution[decision] = distribution.get(decision, 0) + 1

        total = sum(distribution.values())
        percentages = {k: (v / total * 100) if total > 0 else 0 for k, v in distribution.items()}

        return {
            'counts': distribution,
            'percentages': percentages,
            'total_events': total,
        }

    def detect_thermal_trend(self, minutes=30):
        """Detect if temperature is rising (True) or falling (False).

        Calculates slope of temperature over time. Positive slope indicates
        increasing thermal trend, negative indicates cooling.

        Args:
            minutes: Time window for trend analysis (default: 30)

        Returns:
            True if rising, False if falling, None if insufficient data
        """
        since = datetime.now() - timedelta(minutes=minutes)
        events = self.logger.get_events_since(since.timestamp())

        if len(events) < 2:
            return None

        temps = [e['cpu_temp'] for e in events if e['cpu_temp'] is not None]
        if len(temps) < 2:
            return None

        # Calculate slope: if positive, temp is rising
        slope = (temps[-1] - temps[0]) / len(temps)
        return slope > 0.1  # True if rising more than 0.1°C per event

    def get_thermal_statistics(self, hours=1):
        """Get detailed thermal statistics.

        Args:
            hours: Number of hours to analyze (default: 1)

        Returns:
            Dictionary with temp statistics and trend info
        """
        since = datetime.now() - timedelta(hours=hours)
        events = self.logger.get_events_since(since.timestamp())

        if not events:
            return None

        temps = [e['cpu_temp'] for e in events if e['cpu_temp'] is not None]

        if not temps:
            return None

        return {
            'count': len(temps),
            'avg': statistics.mean(temps),
            'median': statistics.median(temps),
            'min': min(temps),
            'max': max(temps),
            'stddev': statistics.stdev(temps) if len(temps) > 1 else 0,
            'trend': self.detect_thermal_trend(minutes=int(hours * 60)),
        }

    def get_performance_metrics(self, hours=1):
        """Get comprehensive performance metrics.

        Args:
            hours: Number of hours to analyze (default: 1)

        Returns:
            Dictionary with all key metrics including temperatures, loads, and decisions
        """
        stats = self.logger.get_statistics(hours=hours)
        dist = self.get_decision_distribution(hours=hours)

        if not stats:
            return None

        return {
            'monitoring_duration_hours': hours,
            'total_events': stats['event_count'],
            'temperatures': stats['temp'],
            'cpu_loads': stats['load'],
            'ram_usage': stats['ram'],
            'decision_distribution': dist,
            'thermal_trend': self.detect_thermal_trend(minutes=int(hours * 60)),
        }

    def get_load_trend(self, minutes=30):
        """Detect if CPU load is increasing (True) or decreasing (False).

        Args:
            minutes: Time window for trend analysis (default: 30)

        Returns:
            True if rising, False if falling, None if insufficient data
        """
        since = datetime.now() - timedelta(minutes=minutes)
        events = self.logger.get_events_since(since.timestamp())

        if len(events) < 2:
            return None

        loads = [e['cpu_load'] for e in events if e['cpu_load'] is not None]
        if len(loads) < 2:
            return None

        slope = (loads[-1] - loads[0]) / len(loads)
        return slope > 0.5  # True if rising more than 0.5% per event

    def get_throttle_impact(self, hours=1):
        """Calculate how much throttling/batching was applied.

        Returns percentage of time spent in BATCH/THROTTLE/EMERGENCY modes.

        Args:
            hours: Number of hours to analyze (default: 1)

        Returns:
            Dictionary with pacing percentage and breakdown by mode
        """
        dist = self.get_decision_distribution(hours=hours)
        counts = dist.get('counts', {})

        total = dist.get('total_events', 0)
        if total == 0:
            return None

        pacing_counts = {
            'BATCH': counts.get('BATCH', 0),
            'THROTTLE': counts.get('THROTTLE', 0),
            'EMERGENCY': counts.get('EMERGENCY', 0),
        }

        pacing_total = sum(pacing_counts.values())
        pacing_pct = (pacing_total / total * 100) if total > 0 else 0

        return {
            'pacing_percentage': pacing_pct,
            'pacing_breakdown': pacing_counts,
            'fullrate_percentage': (counts.get('FULL_RATE', 0) / total * 100) if total > 0 else 0,
        }
