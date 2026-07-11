from infrastructure.nerve_base import NerveBase

class PPVO_104_RayTracingNerve14(NerveBase):
    NERVE_ID = "PPVO_104"
    DEPARTMENT = "PPVO"
    DIVISION = "ray_tracing"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
