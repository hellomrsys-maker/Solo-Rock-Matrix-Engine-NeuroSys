from infrastructure.nerve_base import NerveBase

class SCCN_273_TotalClosureNerve3(NerveBase):
    NERVE_ID = "SCCN_273"
    DEPARTMENT = "SCCN"
    DIVISION = "total_closure"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
