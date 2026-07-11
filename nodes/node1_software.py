"""
Node 1 — Software. The application/runtime side of the symmetric loop:
the entry point for a task request before any executive policy,
balancing, or hardware feedback has touched it.
"""


class Node1Software:
    def __init__(self):
        self.connected_departments = []

    def route_payload(self, payload):
        """Stamp a raw task request as having entered the loop via software."""
        payload.setdefault("trace", []).append("node1_software")
        payload.setdefault("origin", "node1_software")
        return payload
