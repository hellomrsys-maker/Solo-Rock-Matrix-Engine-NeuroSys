from .event_bus import event_bus

class DepartmentAI:
    DEPARTMENT_ID = "UNKNOWN"
    BODY_ANALOGY = "UNKNOWN"

    def __init__(self):
        self.managers = []          # List of ManagerBase instances
        self.is_autonomous = True   # Can make decisions independently

    def register_manager(self, manager):
        self.managers.append(manager)

    def department_health(self):
        return {
            "department": self.DEPARTMENT_ID,
            "managers": len(self.managers),
            "total_nerves": sum(len(m.nerves) for m in self.managers),
            "healthy": all(m.is_healthy for m in self.managers),
        }

    def autonomous_decision(self, local_state):
        """Each department can make its own decisions without asking Central AI."""
        raise NotImplementedError

    def escalate_to_central(self, emergency_data):
        """Only escalate to CEO when department cannot handle alone."""
        event_bus.publish("CENTRAL_ESCALATION", {
            "from": self.DEPARTMENT_ID,
            "data": emergency_data
        })
