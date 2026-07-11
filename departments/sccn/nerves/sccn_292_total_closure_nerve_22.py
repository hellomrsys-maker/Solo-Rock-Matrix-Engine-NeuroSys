from infrastructure.nerve_base import NerveBase

class SCCN_292_TotalClosureNerve22(NerveBase):
    NERVE_ID = "SCCN_292"
    DEPARTMENT = "SCCN"
    DIVISION = "total_closure"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
