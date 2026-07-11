from infrastructure.nerve_base import NerveBase

class SCCN_120_MagentaLoopNerve30(NerveBase):
    NERVE_ID = "SCCN_120"
    DEPARTMENT = "SCCN"
    DIVISION = "magenta_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
