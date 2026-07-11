from infrastructure.nerve_base import NerveBase

class CERN_200_ErrorContainmentNerve20(NerveBase):
    NERVE_ID = "CERN_200"
    DEPARTMENT = "CERN"
    DIVISION = "error_containment"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
