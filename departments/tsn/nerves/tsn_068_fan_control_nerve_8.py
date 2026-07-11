from infrastructure.nerve_base import NerveBase

class TSN_068_FanControlNerve8(NerveBase):
    NERVE_ID = "TSN_068"
    DEPARTMENT = "TSN"
    DIVISION = "fan_control"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
