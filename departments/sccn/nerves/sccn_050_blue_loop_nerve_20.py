from infrastructure.nerve_base import NerveBase

class SCCN_050_BlueLoopNerve20(NerveBase):
    NERVE_ID = "SCCN_050"
    DEPARTMENT = "SCCN"
    DIVISION = "blue_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
