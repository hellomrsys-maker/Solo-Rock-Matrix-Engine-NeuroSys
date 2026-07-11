from infrastructure.nerve_base import NerveBase

class TSN_063_FanControlNerve3(NerveBase):
    NERVE_ID = "TSN_063"
    DEPARTMENT = "TSN"
    DIVISION = "fan_control"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
