from infrastructure.nerve_base import NerveBase

class FSMF_105_RamBusNerve15(NerveBase):
    NERVE_ID = "FSMF_105"
    DEPARTMENT = "FSMF"
    DIVISION = "ram_bus"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
