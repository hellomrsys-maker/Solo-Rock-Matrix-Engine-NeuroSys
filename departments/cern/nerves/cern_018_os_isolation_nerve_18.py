from infrastructure.nerve_base import NerveBase

class CERN_018_OsIsolationNerve18(NerveBase):
    NERVE_ID = "CERN_018"
    DEPARTMENT = "CERN"
    DIVISION = "os_isolation"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
