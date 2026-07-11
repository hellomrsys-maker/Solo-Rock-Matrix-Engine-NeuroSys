from infrastructure.nerve_base import NerveBase

class FSMF_108_RamBusNerve18(NerveBase):
    NERVE_ID = "FSMF_108"
    DEPARTMENT = "FSMF"
    DIVISION = "ram_bus"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
