from infrastructure.nerve_base import NerveBase

class CERN_120_InterruptAuthorityNerve30(NerveBase):
    NERVE_ID = "CERN_120"
    DEPARTMENT = "CERN"
    DIVISION = "interrupt_authority"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
