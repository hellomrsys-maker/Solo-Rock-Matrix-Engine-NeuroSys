from infrastructure.nerve_base import NerveBase

class PDEC_158_RailVoltageNerve8(NerveBase):
    NERVE_ID = "PDEC_158"
    DEPARTMENT = "PDEC"
    DIVISION = "rail_voltage"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
