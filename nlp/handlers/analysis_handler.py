"""Data analysis handler for natural language queries."""

import time
from analytics.query import TelemetryAnalyzer


class AnalysisHandler:
    """Analyzes historical telemetry data based on user queries."""

    def __init__(self):
        """Initialize analysis handler."""
        self.analyzer = TelemetryAnalyzer()

    def handle(self, entities: dict) -> dict:
        """
        Analyze telemetry data based on extracted entities.

        Args:
            entities: Dict with extracted entities (time_range, metrics, etc.)

        Returns:
            dict with analysis results
        """
        try:
            # Get time range from entities (default: 1 hour)
            time_range_hours = entities.get('time_range', 1) or 1

            # Get performance metrics
            metrics = self.analyzer.get_performance_metrics(hours=time_range_hours)

            if not metrics:
                return {
                    'type': 'analysis',
                    'title': 'Analysis Results',
                    'content': f'## Analysis for Last {time_range_hours} Hour(s)\n\nNo data available.',
                    'error': 'No telemetry data available'
                }

            # Detect trends
            thermal_trend = self.analyzer.detect_thermal_trend(minutes=int(time_range_hours * 60))
            load_trend = self.analyzer.get_load_trend(minutes=int(time_range_hours * 60))

            # Get decision distribution
            decision_dist = self.analyzer.get_decision_distribution(hours=time_range_hours)

            # Format analysis results
            content = self._format_analysis(
                time_range_hours,
                metrics,
                thermal_trend,
                load_trend,
                decision_dist
            )

            return {
                'type': 'analysis',
                'title': f'System Analysis — Last {time_range_hours} Hour(s)',
                'content': content,
                'metrics': metrics,
                'thermal_trend': thermal_trend,
                'load_trend': load_trend,
                'decision_distribution': decision_dist,
                'timestamp': time.time(),
                'error': None
            }

        except Exception as e:
            return {
                'type': 'analysis',
                'title': 'Analysis Error',
                'content': f'## Error\n\nFailed to analyze data: {str(e)}',
                'error': str(e)
            }

    def _format_analysis(self, hours: int, metrics: dict, thermal_trend, load_trend, decision_dist: dict) -> str:
        """Format analysis results for display."""
        trend_icon_temp = '📈' if thermal_trend else '📉' if thermal_trend is False else '➡️'
        trend_icon_load = '📈' if load_trend else '📉' if load_trend is False else '➡️'

        trend_text_temp = 'Rising' if thermal_trend else 'Falling' if thermal_trend is False else 'Stable'
        trend_text_load = 'Rising' if load_trend else 'Falling' if load_trend is False else 'Stable'

        temps = metrics.get('temperatures', {})
        loads = metrics.get('cpu_loads', {})
        ram = metrics.get('ram_usage', {})

        # Decision distribution
        dist_counts = decision_dist.get('counts', {})
        dist_pct = decision_dist.get('percentages', {})

        decisions_text = '\n'.join([
            f"  - {decision}: {dist_pct.get(decision, 0):.1f}% ({dist_counts.get(decision, 0)} times)"
            for decision in ['FULL_RATE', 'BATCH', 'THROTTLE', 'EMERGENCY']
        ])

        return f"""
## System Analysis — Last {hours} Hour(s)

### Temperature Analysis
{trend_icon_temp} **Trend:** {trend_text_temp}
- Average: {temps.get('avg', 'N/A')}°C
- Peak: {temps.get('max', 'N/A')}°C
- Valley: {temps.get('min', 'N/A')}°C
- Std Dev: {temps.get('stdev', 'N/A')}°C

### CPU Load Analysis
{trend_icon_load} **Trend:** {trend_text_load}
- Average: {loads.get('avg', 'N/A')}%
- Peak: {loads.get('max', 'N/A')}%
- Minimum: {loads.get('min', 'N/A')}%
- Std Dev: {loads.get('stdev', 'N/A')}%

### RAM Usage
- Average: {ram.get('avg', 'N/A')}%
- Peak: {ram.get('max', 'N/A')}%
- Minimum: {ram.get('min', 'N/A')}%

### Decision Distribution
{decisions_text}

### Summary
- Total events: {metrics.get('total_events', 'N/A')}
- Monitoring duration: {hours} hour(s)
"""

    def get_help_text(self) -> str:
        """Get help text for analysis intent."""
        return """
**Data Analysis**

Analyze historical system trends and patterns.

Examples:
- "analyze the data"
- "show me trends"
- "what changed"
- "analyze trends for the last day"

Shows:
- Temperature trends (rising, falling, stable)
- CPU load patterns
- RAM usage statistics
- Decision distribution (how often each routing mode was active)
- Peak and average metrics over time period
"""
