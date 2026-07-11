from infrastructure.nerve_base import NerveBase

class PDEC_133_ThermalThrottleNerve13(NerveBase):
    NERVE_ID = "PDEC_133"
    DEPARTMENT = "PDEC"
    DIVISION = "thermal_throttle"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
