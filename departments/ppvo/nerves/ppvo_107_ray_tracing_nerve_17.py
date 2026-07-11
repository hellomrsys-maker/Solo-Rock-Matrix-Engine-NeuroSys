from infrastructure.nerve_base import NerveBase

class PPVO_107_RayTracingNerve17(NerveBase):
    NERVE_ID = "PPVO_107"
    DEPARTMENT = "PPVO"
    DIVISION = "ray_tracing"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
