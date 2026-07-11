from infrastructure.nerve_base import NerveBase

class TSN_051_DieTemperatureNerve21(NerveBase):
    NERVE_ID = "TSN_051"
    DEPARTMENT = "TSN"
    DIVISION = "die_temperature"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
