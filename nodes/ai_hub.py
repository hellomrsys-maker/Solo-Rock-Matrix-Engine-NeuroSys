"""
The AI Hub — center of the four-node symmetric ring described in
architectural_specification.md (Chapter 3). Any of the four nodes may
initiate a routing cycle; the hub just chains the remaining three in
the order that mode implies. All four orders visit the same four
nodes and converge on the same `final_action`, which is exactly the
point: there is no single top-down path, so a busy or hot hardware
layer can always get its back-pressure heard regardless of who asked.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodes.node1_software import Node1Software
from nodes.node2_executive import Node2Executive
from nodes.node3_balance import Node3Balance
from nodes.node4_hardware import Node4Hardware

# The four permutation modes from Chapter 3 of the architectural spec:
#   1=2=3=4=AI  Software-driven   : app submits work
#   2=3=4=1=AI  Executive-driven  : CEO reallocates priorities
#   3=4=1=2=AI  Balance-driven    : load balancer reroutes on its own
#   4=1=2=3=AI  Hardware-driven   : silicon back-pressure leads
MODE_ORDERS = {
    "software_driven": ("node1", "node2", "node3", "node4"),
    "executive_driven": ("node2", "node3", "node4", "node1"),
    "balance_driven": ("node3", "node4", "node1", "node2"),
    "hardware_driven": ("node4", "node1", "node2", "node3"),
}


class AiHub:
    def __init__(self, central_ai=None):
        self.central_ai = central_ai
        self.nodes = {
            "node1": Node1Software(),
            "node2": Node2Executive(central_ai=central_ai),
            "node3": Node3Balance(),
            "node4": Node4Hardware(central_ai=central_ai),
        }
        self.connected_departments = []

    def register_department(self, department):
        """Wire a DepartmentAI into the balance node so it participates in routing."""
        self.nodes["node3"].register_department(department)
        self.connected_departments.append(department)

    def dispatch(self, payload, mode="software_driven"):
        """
        Route a task payload through the ring in the order implied by `mode`.
        Returns the payload after all four nodes have annotated it, with
        `final_action` set by Node 4 based on the Central AI's live decision.
        """
        order = MODE_ORDERS.get(mode, MODE_ORDERS["software_driven"])
        payload.setdefault("mode", mode)
        for node_name in order:
            payload = self.nodes[node_name].route_payload(payload)
        return payload

    def route_payload(self, payload):
        """Default entry point: software-driven dispatch."""
        return self.dispatch(payload, mode="software_driven")


if __name__ == "__main__":
    from central_command.central_ai import CentralAI

    ceo = CentralAI()
    hub = AiHub(central_ai=ceo)

    for mode in MODE_ORDERS:
        task = {"task_id": "demo-task", "workload_type": "compute", "priority": 1}
        result = hub.dispatch(task, mode=mode)
        print(f"[{mode}] trace={result['trace']} -> final_action={result['final_action']}")
