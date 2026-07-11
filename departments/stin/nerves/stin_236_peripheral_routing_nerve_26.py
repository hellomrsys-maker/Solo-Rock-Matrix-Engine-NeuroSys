from infrastructure.nerve_base import NerveBase

class STIN_236_PeripheralRoutingNerve26(NerveBase):
    NERVE_ID = "STIN_236"
    DEPARTMENT = "STIN"
    DIVISION = "peripheral_routing"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
