"""Report generation handler for natural language queries."""

import time
from report import ReportGenerator


class ReportHandler:
    """Generates system reports based on user queries."""

    def __init__(self):
        """Initialize report handler."""
        self.generator = ReportGenerator()

    def handle(self, entities: dict) -> dict:
        """
        Generate report based on extracted entities.

        Args:
            entities: Dict with extracted entities (time_range, metrics, etc.)

        Returns:
            dict with:
                - type: 'report'
                - title: Report title (str)
                - content: Report content in markdown (str)
                - format: Output format (markdown, json, html)
        """
        try:
            # Generate report with default or specified time range
            # For now, generate full dynamic report
            report_data = self.generator.generate()

            if report_data is None or not report_data:
                return {
                    'type': 'report',
                    'title': 'System Report',
                    'content': '## System Report\n\nNo data available. Start monitoring to generate reports.',
                    'format': 'markdown',
                    'error': 'No telemetry data available'
                }

            # Convert report to markdown text
            report_text = self.generator.to_text()

            return {
                'type': 'report',
                'title': 'SOLO ROCK System Report',
                'content': report_text,
                'format': 'markdown',
                'timestamp': time.time(),
                'error': None
            }

        except Exception as e:
            return {
                'type': 'report',
                'title': 'Error Generating Report',
                'content': f'## Error\n\nFailed to generate report: {str(e)}',
                'format': 'markdown',
                'error': str(e)
            }

    def get_help_text(self) -> str:
        """Get help text for report intent."""
        return """
**Report Generation**

Generate system reports with telemetry summaries.

Examples:
- "show me a report"
- "generate a summary"
- "what happened last hour"
- "create a detailed report"

Reports include:
- System health status
- Temperature and load metrics
- Decision distribution (FULL_RATE, BATCH, THROTTLE, EMERGENCY)
- Thermal and load trends
- Recommended actions
"""
