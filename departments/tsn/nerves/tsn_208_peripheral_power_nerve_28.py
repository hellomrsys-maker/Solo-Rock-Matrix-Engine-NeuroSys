from infrastructure.nerve_base import NerveBase

class TSN_208_PeripheralPowerNerve28(NerveBase):
    NERVE_ID = "TSN_208"
    DEPARTMENT = "TSN"
    DIVISION = "peripheral_power"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
