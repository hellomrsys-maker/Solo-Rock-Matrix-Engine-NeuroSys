"""Intent detection for natural language queries — maps user input to system intents."""


class IntentDetector:
    """Detects user intent from natural language queries using keyword matching."""

    # Intent keywords mapping
    INTENT_KEYWORDS = {
        'report': ['show', 'report', 'generate', 'what happened', 'summary', 'tell me'],
        'status': ['status', 'how', 'working', 'ok', 'health', 'current', 'now'],
        'analysis': ['analyze', 'trends', 'changed', 'pattern', 'history', 'data'],
        'alert': ['alert', 'notify', 'send', 'subscribe', 'notification', 'email', 'slack'],
        'config': ['change', 'update', 'set', 'threshold', 'configure', 'adjust'],
        'help': ['help', 'what can', 'example', 'how do', 'how to'],
    }

    def __init__(self):
        """Initialize intent detector with keyword mappings."""
        self.intent_keywords = self.INTENT_KEYWORDS

    def detect(self, query: str) -> dict:
        """
        Detect intent from user query.

        Args:
            query: User input string

        Returns:
            dict with keys:
                - intent: detected intent name (str)
                - confidence: confidence score 0.0-1.0 (float)
                - matched_keywords: list of keywords that matched (list)
        """
        query_lower = query.lower()

        # Score each intent based on keyword matches
        intent_scores = {}
        for intent, keywords in self.intent_keywords.items():
            matched = [kw for kw in keywords if kw in query_lower]
            if matched:
                score = len(matched) / len(keywords)  # Proportion of keywords matched
                intent_scores[intent] = {
                    'score': score,
                    'matched': matched
                }

        # Return top intent, or 'unknown' if no matches
        if not intent_scores:
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'matched_keywords': []
            }

        top_intent = max(intent_scores.items(), key=lambda x: x[1]['score'])
        return {
            'intent': top_intent[0],
            'confidence': min(top_intent[1]['score'], 1.0),
            'matched_keywords': top_intent[1]['matched']
        }

    def get_example_queries(self, intent: str = None) -> list:
        """
        Get example queries for an intent.

        Args:
            intent: Intent name, or None for all intents

        Returns:
            List of example queries
        """
        examples = {
            'report': [
                'show me a report',
                'generate a summary',
                'what happened last hour',
                'create a detailed report',
            ],
            'status': [
                'how is it working',
                'what is the current status',
                'is everything ok',
                'show me the status',
            ],
            'analysis': [
                'analyze the data',
                'show me trends',
                'what changed',
                'analyze trends for the last day',
            ],
            'alert': [
                'set up email alerts',
                'enable slack notifications',
                'alert me on emergency',
                'send alerts to email@example.com',
            ],
            'config': [
                'change thermal warning to 75',
                'update cpu threshold',
                'set critical temperature to 90',
            ],
            'help': [
                'what can you do',
                'show examples',
                'help me',
                'how do I use this',
            ],
        }

        if intent and intent in examples:
            return examples[intent]

        # Return all examples
        all_examples = []
        for exs in examples.values():
            all_examples.extend(exs)
        return all_examples
