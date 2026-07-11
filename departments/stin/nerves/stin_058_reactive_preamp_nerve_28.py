from infrastructure.nerve_base import NerveBase

class STIN_058_ReactivePreampNerve28(NerveBase):
    NERVE_ID = "STIN_058"
    DEPARTMENT = "STIN"
    DIVISION = "reactive_preamp"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
