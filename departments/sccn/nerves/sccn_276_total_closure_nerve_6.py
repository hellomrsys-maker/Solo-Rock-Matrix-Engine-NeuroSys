from infrastructure.nerve_base import NerveBase

class SCCN_276_TotalClosureNerve6(NerveBase):
    NERVE_ID = "SCCN_276"
    DEPARTMENT = "SCCN"
    DIVISION = "total_closure"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
