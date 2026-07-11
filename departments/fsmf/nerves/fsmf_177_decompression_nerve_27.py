from infrastructure.nerve_base import NerveBase

class FSMF_177_DecompressionNerve27(NerveBase):
    NERVE_ID = "FSMF_177"
    DEPARTMENT = "FSMF"
    DIVISION = "decompression"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
