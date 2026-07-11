from infrastructure.nerve_base import NerveBase

class CERN_291_GlobalCoordinationNerve21(NerveBase):
    NERVE_ID = "CERN_291"
    DEPARTMENT = "CERN"
    DIVISION = "global_coordination"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
