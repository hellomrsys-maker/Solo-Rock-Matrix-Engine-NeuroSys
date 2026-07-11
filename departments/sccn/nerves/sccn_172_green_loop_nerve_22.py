from infrastructure.nerve_base import NerveBase

class SCCN_172_GreenLoopNerve22(NerveBase):
    NERVE_ID = "SCCN_172"
    DEPARTMENT = "SCCN"
    DIVISION = "green_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
