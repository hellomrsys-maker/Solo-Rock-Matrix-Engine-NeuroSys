class WireRegistry:
    def __init__(self):
        self._nerves_by_wire = {
            "yellow": [],
            "teal": [],
            "dark_red": [],
            "pink": [],
            "orange": [],
            "green": [],
            "purple": [],
            "blue": [],
            "magenta": [],
            "all": [] # Used for SCCN Total Closure
        }

    def register(self, nerve):
        if nerve.WIRE_COLOR in self._nerves_by_wire:
            self._nerves_by_wire[nerve.WIRE_COLOR].append(nerve)
        elif nerve.WIRE_COLOR == "ALL" or nerve.WIRE_COLOR == "all":
             self._nerves_by_wire["all"].append(nerve)
            
    def get_nerves(self, wire_color):
        return self._nerves_by_wire.get(wire_color, [])

# Global registry
wire_registry = WireRegistry()
