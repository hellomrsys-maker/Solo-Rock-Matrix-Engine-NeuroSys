from infrastructure.nerve_base import NerveBase

class CERN_274_GlobalCoordinationNerve4(NerveBase):
    NERVE_ID = "CERN_274"
    DEPARTMENT = "CERN"
    DIVISION = "global_coordination"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
