"""
Node 4 — Hardware. The physical-silicon side of the loop. Reads live
telemetry through the Central AI's Global State Vector and turns it
into back-pressure the software layer can actually see, instead of
staying silent while it throttles internally.
"""

FINAL_ACTIONS = {
    "FULL_RATE": "DISPATCH",
    "BATCH": "DISPATCH_BATCHED",
    "THROTTLE": "HOLD",
    "EMERGENCY": "REJECT",
}


class Node4Hardware:
    def __init__(self, central_ai=None):
        self.connected_departments = []
        self.central_ai = central_ai

    def route_payload(self, payload):
        payload.setdefault("trace", []).append("node4_hardware")

        if self.central_ai is not None:
            action = self.central_ai.last_action or self.central_ai.tick()[0]
        else:
            action = payload.get("executive_policy", "FULL_RATE")

        payload["hardware_backpressure"] = action in ("THROTTLE", "EMERGENCY")
        payload["final_action"] = FINAL_ACTIONS.get(action, "DISPATCH")
        return payload
