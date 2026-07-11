from infrastructure.nerve_base import NerveBase

class CERN_155_ThermalPredictionNerve5(NerveBase):
    NERVE_ID = "CERN_155"
    DEPARTMENT = "CERN"
    DIVISION = "thermal_prediction"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
