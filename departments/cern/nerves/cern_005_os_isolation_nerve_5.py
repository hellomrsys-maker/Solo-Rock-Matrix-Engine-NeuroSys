from infrastructure.nerve_base import NerveBase

class CERN_005_OsIsolationNerve5(NerveBase):
    NERVE_ID = "CERN_005"
    DEPARTMENT = "CERN"
    DIVISION = "os_isolation"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
