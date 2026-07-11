from infrastructure.nerve_base import NerveBase

class PDEC_127_ThermalThrottleNerve7(NerveBase):
    NERVE_ID = "PDEC_127"
    DEPARTMENT = "PDEC"
    DIVISION = "thermal_throttle"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
