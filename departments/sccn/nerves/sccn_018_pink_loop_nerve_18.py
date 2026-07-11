from infrastructure.nerve_base import NerveBase

class SCCN_018_PinkLoopNerve18(NerveBase):
    NERVE_ID = "SCCN_018"
    DEPARTMENT = "SCCN"
    DIVISION = "pink_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
