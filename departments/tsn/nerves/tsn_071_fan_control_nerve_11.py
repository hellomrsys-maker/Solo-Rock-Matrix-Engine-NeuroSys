from infrastructure.nerve_base import NerveBase

class TSN_071_FanControlNerve11(NerveBase):
    NERVE_ID = "TSN_071"
    DEPARTMENT = "TSN"
    DIVISION = "fan_control"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
