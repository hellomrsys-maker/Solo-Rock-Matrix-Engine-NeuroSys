from infrastructure.nerve_base import NerveBase

class PPVO_120_RayTracingNerve30(NerveBase):
    NERVE_ID = "PPVO_120"
    DEPARTMENT = "PPVO"
    DIVISION = "ray_tracing"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
