from infrastructure.nerve_base import NerveBase

class PDEC_182_CapacitorNerve2(NerveBase):
    NERVE_ID = "PDEC_182"
    DEPARTMENT = "PDEC"
    DIVISION = "capacitor"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
