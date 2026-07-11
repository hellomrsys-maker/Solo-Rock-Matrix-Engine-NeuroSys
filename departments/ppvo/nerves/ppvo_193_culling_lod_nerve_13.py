from infrastructure.nerve_base import NerveBase

class PPVO_193_CullingLodNerve13(NerveBase):
    NERVE_ID = "PPVO_193"
    DEPARTMENT = "PPVO"
    DIVISION = "culling_lod"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
