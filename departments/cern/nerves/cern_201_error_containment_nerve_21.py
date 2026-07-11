from infrastructure.nerve_base import NerveBase

class CERN_201_ErrorContainmentNerve21(NerveBase):
    NERVE_ID = "CERN_201"
    DEPARTMENT = "CERN"
    DIVISION = "error_containment"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
