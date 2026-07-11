from infrastructure.nerve_base import NerveBase

class FSMF_120_RamBusNerve30(NerveBase):
    NERVE_ID = "FSMF_120"
    DEPARTMENT = "FSMF"
    DIVISION = "ram_bus"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
