class NerveRegistry:
    def __init__(self):
        self._nerves = {}

    def register(self, nerve):
        if nerve.NERVE_ID in self._nerves:
            # We allow overriding if restarting/re-registering, but usually it should be unique
            pass
        self._nerves[nerve.NERVE_ID] = nerve

    def get_nerve(self, nerve_id):
        return self._nerves.get(nerve_id)

    def get_all_nerves(self):
        return list(self._nerves.values())
        
    def get_nerves_by_department(self, dept_id):
        return [n for n in self._nerves.values() if n.DEPARTMENT == dept_id]

# Global registry
nerve_registry = NerveRegistry()
