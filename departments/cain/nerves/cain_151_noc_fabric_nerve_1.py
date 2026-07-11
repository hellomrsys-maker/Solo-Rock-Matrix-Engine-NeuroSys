from infrastructure.nerve_base import NerveBase

class CAIN_151_NocFabricNerve1(NerveBase):
    NERVE_ID = "CAIN_151"
    DEPARTMENT = "CAIN"
    DIVISION = "noc_fabric"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
