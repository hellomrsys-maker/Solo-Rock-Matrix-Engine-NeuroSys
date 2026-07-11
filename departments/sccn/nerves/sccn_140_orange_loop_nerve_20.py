from infrastructure.nerve_base import NerveBase

class SCCN_140_OrangeLoopNerve20(NerveBase):
    NERVE_ID = "SCCN_140"
    DEPARTMENT = "SCCN"
    DIVISION = "orange_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
