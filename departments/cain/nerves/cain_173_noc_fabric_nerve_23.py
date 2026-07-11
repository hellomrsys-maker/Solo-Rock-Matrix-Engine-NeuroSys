from infrastructure.nerve_base import NerveBase

class CAIN_173_NocFabricNerve23(NerveBase):
    NERVE_ID = "CAIN_173"
    DEPARTMENT = "CAIN"
    DIVISION = "noc_fabric"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
