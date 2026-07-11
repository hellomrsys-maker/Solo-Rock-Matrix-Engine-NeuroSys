from infrastructure.nerve_base import NerveBase

class SCCN_200_PurpleLoopNerve20(NerveBase):
    NERVE_ID = "SCCN_200"
    DEPARTMENT = "SCCN"
    DIVISION = "purple_loop"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
