from infrastructure.nerve_base import NerveBase

class CAIN_171_NocFabricNerve21(NerveBase):
    NERVE_ID = "CAIN_171"
    DEPARTMENT = "CAIN"
    DIVISION = "noc_fabric"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
