class ManagerBase:
    MANAGER_ID = "UNKNOWN"
    DEPARTMENT = "UNKNOWN"
    DIVISION = "UNKNOWN"

    def __init__(self):
        self.nerves = []            # List of NerveBase instances
        self.is_healthy = True

    def register_nerve(self, nerve):
        self.nerves.append(nerve)

    def fire_all(self, payload):
        """Fire all nerves in this division simultaneously."""
        for nerve in self.nerves:
            nerve._on_signal(payload)

    def health_check(self):
        return {
            "manager": self.MANAGER_ID,
            "nerve_count": len(self.nerves),
            "all_alive": all(n.is_alive for n in self.nerves),
            "total_fires": sum(n.fire_count for n in self.nerves),
        }
