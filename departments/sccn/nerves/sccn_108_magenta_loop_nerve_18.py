from infrastructure.nerve_base import NerveBase

class SCCN_108_MagentaLoopNerve18(NerveBase):
    NERVE_ID = "SCCN_108"
    DEPARTMENT = "SCCN"
    DIVISION = "magenta_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
