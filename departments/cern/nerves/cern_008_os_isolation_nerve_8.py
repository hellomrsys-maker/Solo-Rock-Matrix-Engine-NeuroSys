from infrastructure.nerve_base import NerveBase

class CERN_008_OsIsolationNerve8(NerveBase):
    NERVE_ID = "CERN_008"
    DEPARTMENT = "CERN"
    DIVISION = "os_isolation"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
