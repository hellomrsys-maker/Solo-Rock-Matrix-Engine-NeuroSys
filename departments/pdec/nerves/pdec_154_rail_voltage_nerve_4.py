from infrastructure.nerve_base import NerveBase

class PDEC_154_RailVoltageNerve4(NerveBase):
    NERVE_ID = "PDEC_154"
    DEPARTMENT = "PDEC"
    DIVISION = "rail_voltage"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
