from infrastructure.nerve_base import NerveBase

class PPVO_206_CullingLodNerve26(NerveBase):
    NERVE_ID = "PPVO_206"
    DEPARTMENT = "PPVO"
    DIVISION = "culling_lod"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
