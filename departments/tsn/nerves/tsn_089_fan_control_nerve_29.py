from infrastructure.nerve_base import NerveBase

class TSN_089_FanControlNerve29(NerveBase):
    NERVE_ID = "TSN_089"
    DEPARTMENT = "TSN"
    DIVISION = "fan_control"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
