from infrastructure.nerve_base import NerveBase

class STIN_250_PressureMappingNerve10(NerveBase):
    NERVE_ID = "STIN_250"
    DEPARTMENT = "STIN"
    DIVISION = "pressure_mapping"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
