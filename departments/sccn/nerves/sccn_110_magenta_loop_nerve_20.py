from infrastructure.nerve_base import NerveBase

class SCCN_110_MagentaLoopNerve20(NerveBase):
    NERVE_ID = "SCCN_110"
    DEPARTMENT = "SCCN"
    DIVISION = "magenta_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
