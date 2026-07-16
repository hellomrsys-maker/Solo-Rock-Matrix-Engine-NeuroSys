"""Query processor orchestrating intent detection, entity extraction, and handler execution."""

from nlp.intent_detector import IntentDetector
from nlp.entity_extractor import EntityExtractor
from nlp.handlers import ReportHandler, StatusHandler, AnalysisHandler, HelpHandler


class QueryProcessor:
    """Processes natural language queries end-to-end."""

    def __init__(self):
        """Initialize query processor with components."""
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractor()

        # Initialize handlers
        self.handlers = {
            'report': ReportHandler(),
            'status': StatusHandler(),
            'analysis': AnalysisHandler(),
            'help': HelpHandler(),
            'unknown': HelpHandler(),  # Show help for unknown intents
        }

    def process(self, query: str) -> dict:
        """
        Process user query end-to-end.

        Args:
            query: User input string

        Returns:
            dict with:
                - intent: Detected intent (str)
                - confidence: Confidence score 0.0-1.0
                - type: Response type (report, status, analysis, help)
                - title: Response title
                - content: Response content (markdown)
                - display_type: How to display (text, markdown, chart)
                - error: Error message if any
        """
        try:
            # Step 1: Detect intent
            intent_result = self.intent_detector.detect(query)
            intent = intent_result['intent']
            confidence = intent_result['confidence']

            # Step 2: Extract entities
            entities = self.entity_extractor.extract(query)

            # Step 3: Route to appropriate handler
            handler = self.handlers.get(intent)
            if not handler:
                handler = self.handlers['unknown']

            # Step 4: Execute handler
            handler_result = handler.handle(entities)

            # Step 5: Format response
            response = {
                'intent': intent,
                'confidence': confidence,
                'type': handler_result.get('type'),
                'title': handler_result.get('title', 'Response'),
                'content': handler_result.get('content', ''),
                'display_type': self._get_display_type(handler_result),
                'timestamp': handler_result.get('timestamp'),
                'error': handler_result.get('error'),
                'raw_result': handler_result,  # For advanced usage
            }

            return response

        except Exception as e:
            return {
                'intent': 'error',
                'confidence': 0.0,
                'type': 'error',
                'title': 'Processing Error',
                'content': f'Error processing query: {str(e)}',
                'display_type': 'text',
                'error': str(e),
            }

    def _get_display_type(self, handler_result: dict) -> str:
        """Determine how to display the result."""
        response_type = handler_result.get('type')

        if response_type == 'report':
            return 'markdown'
        elif response_type == 'status':
            return 'metrics'  # Show as card/metrics
        elif response_type == 'analysis':
            return 'markdown'  # Could also include charts
        else:
            return 'text'

    def get_examples(self) -> dict:
        """Get example queries organized by intent."""
        examples = {}

        # Get examples from intent detector
        for intent in ['report', 'status', 'analysis', 'alert', 'config', 'help']:
            examples[intent] = self.intent_detector.get_example_queries(intent)

        return examples

    def format_help(self) -> str:
        """Get formatted help text."""
        help_handler = self.handlers['help']
        return help_handler.get_help_text()

    def get_suggestions(self) -> list:
        """Get quick start suggestions for user."""
        return [
            "show me a report",
            "how is it working",
            "analyze trends",
            "what's the status",
        ]
