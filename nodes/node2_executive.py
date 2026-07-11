"""
Node 2 — Executive. Applies the Central AI's current routing policy
(FULL_RATE / BATCH / THROTTLE / EMERGENCY) to a task before it reaches
the balance and hardware nodes.
"""


class Node2Executive:
    def __init__(self, central_ai=None):
        self.connected_departments = []
        self.central_ai = central_ai

    def route_payload(self, payload):
        payload.setdefault("trace", []).append("node2_executive")

        if self.central_ai is not None:
            action = self.central_ai.last_action or self.central_ai.tick()[0]
            payload["executive_policy"] = action
        else:
            payload["executive_policy"] = "FULL_RATE"

        return payload
