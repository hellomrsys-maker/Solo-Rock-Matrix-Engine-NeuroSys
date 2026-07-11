from infrastructure.nerve_base import NerveBase

class PDEC_205_CapacitorNerve25(NerveBase):
    NERVE_ID = "PDEC_205"
    DEPARTMENT = "PDEC"
    DIVISION = "capacitor"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
