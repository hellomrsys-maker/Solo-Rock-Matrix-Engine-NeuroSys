from infrastructure.nerve_base import NerveBase

class PPVO_300_ShadowLightingNerve30(NerveBase):
    NERVE_ID = "PPVO_300"
    DEPARTMENT = "PPVO"
    DIVISION = "shadow_lighting"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
