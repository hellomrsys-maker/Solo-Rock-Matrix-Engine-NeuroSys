"""Entity extraction for natural language queries — extracts structured data from user input."""

import re


class EntityExtractor:
    """Extracts entities (time range, metrics, etc.) from natural language queries."""

    # Time range mappings
    TIME_RANGES = {
        'last hour': 1,
        'last 1 hour': 1,
        'past hour': 1,
        '1 hour': 1,
        'last day': 24,
        'last 1 day': 24,
        'past day': 24,
        '1 day': 24,
        'last week': 168,
        'last 1 week': 168,
        'past week': 168,
        '1 week': 168,
        'last month': 720,
        'last 30 days': 720,
    }

    # Metric mappings
    METRICS = {
        'temperature': 'temperature',
        'temp': 'temperature',
        'thermal': 'temperature',
        'cpu load': 'cpu_load',
        'load': 'cpu_load',
        'ram': 'ram_usage',
        'memory': 'ram_usage',
        'gpu': 'gpu_load',
        'battery': 'battery',
    }

    # Decision keywords
    DECISIONS = {
        'full rate': 'FULL_RATE',
        'full-rate': 'FULL_RATE',
        'batch': 'BATCH',
        'throttle': 'THROTTLE',
        'emergency': 'EMERGENCY',
    }

    def __init__(self):
        """Initialize entity extractor."""
        self.time_ranges = self.TIME_RANGES
        self.metrics = self.METRICS
        self.decisions = self.DECISIONS

    def extract(self, query: str) -> dict:
        """
        Extract entities from user query.

        Args:
            query: User input string

        Returns:
            dict with extracted entities:
                - time_range: hours (int) or None
                - metrics: list of metric names or None
                - decisions: list of decision names or None
                - threshold_value: int or None (for config changes)
                - threshold_name: str or None (for config changes)
        """
        query_lower = query.lower()

        entities = {
            'time_range': self._extract_time_range(query_lower),
            'metrics': self._extract_metrics(query_lower),
            'decisions': self._extract_decisions(query_lower),
            'config': self._extract_config(query_lower),
        }

        return entities

    def _extract_time_range(self, query: str) -> int:
        """Extract time range from query."""
        for range_str, hours in self.time_ranges.items():
            if range_str in query:
                return hours
        return None

    def _extract_metrics(self, query: str) -> list:
        """Extract metrics mentioned in query."""
        metrics = []
        for metric_str, metric_name in self.metrics.items():
            if metric_str in query:
                if metric_name not in metrics:
                    metrics.append(metric_name)
        return metrics if metrics else None

    def _extract_decisions(self, query: str) -> list:
        """Extract decision names mentioned in query."""
        decisions = []
        for decision_str, decision_name in self.decisions.items():
            if decision_str in query:
                if decision_name not in decisions:
                    decisions.append(decision_name)
        return decisions if decisions else None

    def _extract_config(self, query: str) -> dict:
        """Extract configuration changes (e.g., 'set thermal warning to 75')."""
        config = {}

        # Pattern: "set <threshold> to <value>"
        pattern = r'(?:set|change|update|adjust)\s+(\w+(?:\s+\w+)?)\s+(?:to|at)\s+(\d+)'
        matches = re.findall(pattern, query, re.IGNORECASE)

        if matches:
            for threshold_name, value in matches:
                config['name'] = threshold_name.lower().strip()
                config['value'] = int(value)

        return config if config else None

    def get_available_metrics(self) -> list:
        """Get list of available metrics."""
        return list(set(self.metrics.values()))

    def get_available_decisions(self) -> list:
        """Get list of available decisions."""
        return list(self.decisions.values())

    def get_available_time_ranges(self) -> dict:
        """Get available time range strings and their hour values."""
        return self.time_ranges.copy()
