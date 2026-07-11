from infrastructure.nerve_base import NerveBase

class TSN_032_DieTemperatureNerve2(NerveBase):
    NERVE_ID = "TSN_032"
    DEPARTMENT = "TSN"
    DIVISION = "die_temperature"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
