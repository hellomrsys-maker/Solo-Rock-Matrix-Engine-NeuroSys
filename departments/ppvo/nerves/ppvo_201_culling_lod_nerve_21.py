from infrastructure.nerve_base import NerveBase

class PPVO_201_CullingLodNerve21(NerveBase):
    NERVE_ID = "PPVO_201"
    DEPARTMENT = "PPVO"
    DIVISION = "culling_lod"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
