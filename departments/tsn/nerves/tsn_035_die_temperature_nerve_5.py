from infrastructure.nerve_base import NerveBase

class TSN_035_DieTemperatureNerve5(NerveBase):
    NERVE_ID = "TSN_035"
    DEPARTMENT = "TSN"
    DIVISION = "die_temperature"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
