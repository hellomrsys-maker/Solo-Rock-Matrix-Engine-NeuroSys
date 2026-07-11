from infrastructure.nerve_base import NerveBase

class PDEC_120_PowerRoutingNerve30(NerveBase):
    NERVE_ID = "PDEC_120"
    DEPARTMENT = "PDEC"
    DIVISION = "power_routing"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
