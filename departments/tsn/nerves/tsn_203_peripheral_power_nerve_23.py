from infrastructure.nerve_base import NerveBase

class TSN_203_PeripheralPowerNerve23(NerveBase):
    NERVE_ID = "TSN_203"
    DEPARTMENT = "TSN"
    DIVISION = "peripheral_power"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
