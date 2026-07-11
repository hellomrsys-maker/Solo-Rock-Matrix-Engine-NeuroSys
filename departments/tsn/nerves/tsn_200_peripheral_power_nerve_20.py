from infrastructure.nerve_base import NerveBase

class TSN_200_PeripheralPowerNerve20(NerveBase):
    NERVE_ID = "TSN_200"
    DEPARTMENT = "TSN"
    DIVISION = "peripheral_power"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
