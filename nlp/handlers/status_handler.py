"""System status handler for natural language queries."""

import time
from central_command.central_ai import CentralAI


class StatusHandler:
    """Returns current system status based on user queries."""

    def __init__(self):
        """Initialize status handler."""
        self.ceo = CentralAI()

    def handle(self, entities: dict) -> dict:
        """
        Get current system status.

        Args:
            entities: Dict with extracted entities (not used for status)

        Returns:
            dict with current system state
        """
        try:
            # Get current telemetry and decision
            action, reason, snapshot = self.ceo.tick()

            # Determine system health
            cpu_temp = snapshot.get('cpu_temp', 0)
            cpu_load = snapshot.get('cpu_load', 0)
            ram_usage = snapshot.get('ram_usage', 0)

            if action == 'EMERGENCY':
                status = '🚨 CRITICAL'
                health = 'Critical — Emergency throttling active'
            elif action == 'THROTTLE':
                status = '⚠️ WARNING'
                health = 'Degraded — System throttling active'
            elif action == 'BATCH':
                status = '⚡ OPTIMIZED'
                health = 'Optimal — Batching dispatch'
            else:  # FULL_RATE
                status = '✅ HEALTHY'
                health = 'Healthy — Full dispatch rate'

            return {
                'type': 'status',
                'status': status,
                'health': health,
                'metrics': {
                    'cpu_temp_celsius': round(cpu_temp, 1),
                    'cpu_load_percent': round(cpu_load, 1),
                    'ram_usage_percent': round(ram_usage, 1),
                    'battery_percent': snapshot.get('battery', None),
                },
                'decision': action,
                'reason': reason,
                'timestamp': time.time(),
                'error': None
            }

        except Exception as e:
            return {
                'type': 'status',
                'status': '❌ ERROR',
                'health': f'Error retrieving status: {str(e)}',
                'error': str(e)
            }

    def format_for_display(self, status_dict: dict) -> str:
        """
        Format status dict for display.

        Args:
            status_dict: Status dict from handle()

        Returns:
            Formatted markdown string
        """
        if status_dict.get('error'):
            return f"## System Status\n\n❌ Error: {status_dict['error']}"

        metrics = status_dict.get('metrics', {})
        return f"""
## System Status: {status_dict['status']}

**Health:** {status_dict['health']}

**Metrics:**
- CPU Temperature: {metrics.get('cpu_temp_celsius', 'N/A')}°C
- CPU Load: {metrics.get('cpu_load_percent', 'N/A')}%
- RAM Usage: {metrics.get('ram_usage_percent', 'N/A')}%
- Battery: {metrics.get('battery_percent', 'N/A')}%

**Current Decision:** {status_dict['decision']}
**Reason:** {status_dict['reason']}
"""

    def get_help_text(self) -> str:
        """Get help text for status intent."""
        return """
**System Status**

Get current system health and metrics.

Examples:
- "how is it working"
- "what is the current status"
- "is everything ok"
- "show me the status"

Shows:
- Overall system health (Healthy, Optimized, Warning, Critical)
- Current temperature, load, memory usage
- Active routing decision (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
- Reason for current decision
"""
