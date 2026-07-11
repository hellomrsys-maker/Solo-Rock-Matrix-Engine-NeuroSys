from infrastructure.nerve_base import NerveBase

class CAIN_180_NocFabricNerve30(NerveBase):
    NERVE_ID = "CAIN_180"
    DEPARTMENT = "CAIN"
    DIVISION = "noc_fabric"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
