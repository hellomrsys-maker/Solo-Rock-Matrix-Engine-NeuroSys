from infrastructure.nerve_base import NerveBase

class SCCN_300_TotalClosureNerve30(NerveBase):
    NERVE_ID = "SCCN_300"
    DEPARTMENT = "SCCN"
    DIVISION = "total_closure"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
