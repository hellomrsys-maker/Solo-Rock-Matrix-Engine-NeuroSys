from infrastructure.nerve_base import NerveBase

class SCCN_017_PinkLoopNerve17(NerveBase):
    NERVE_ID = "SCCN_017"
    DEPARTMENT = "SCCN"
    DIVISION = "pink_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
