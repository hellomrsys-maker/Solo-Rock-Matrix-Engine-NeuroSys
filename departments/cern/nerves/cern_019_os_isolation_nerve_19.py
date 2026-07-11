from infrastructure.nerve_base import NerveBase

class CERN_019_OsIsolationNerve19(NerveBase):
    NERVE_ID = "CERN_019"
    DEPARTMENT = "CERN"
    DIVISION = "os_isolation"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
