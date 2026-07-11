from infrastructure.nerve_base import NerveBase

class CERN_015_OsIsolationNerve15(NerveBase):
    NERVE_ID = "CERN_015"
    DEPARTMENT = "CERN"
    DIVISION = "os_isolation"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
