from infrastructure.nerve_base import NerveBase

class CAIN_195_DmaArbitrationNerve15(NerveBase):
    NERVE_ID = "CAIN_195"
    DEPARTMENT = "CAIN"
    DIVISION = "dma_arbitration"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
