from infrastructure.nerve_base import NerveBase

class TSN_066_FanControlNerve6(NerveBase):
    NERVE_ID = "TSN_066"
    DEPARTMENT = "TSN"
    DIVISION = "fan_control"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
