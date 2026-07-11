from infrastructure.nerve_base import NerveBase

class PDEC_126_ThermalThrottleNerve6(NerveBase):
    NERVE_ID = "PDEC_126"
    DEPARTMENT = "PDEC"
    DIVISION = "thermal_throttle"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
