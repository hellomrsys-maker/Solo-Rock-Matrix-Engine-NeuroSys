from infrastructure.nerve_base import NerveBase

class PPVO_112_RayTracingNerve22(NerveBase):
    NERVE_ID = "PPVO_112"
    DEPARTMENT = "PPVO"
    DIVISION = "ray_tracing"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
