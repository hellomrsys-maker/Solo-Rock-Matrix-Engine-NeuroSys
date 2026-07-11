from infrastructure.nerve_base import NerveBase

class STIN_242_PressureMappingNerve2(NerveBase):
    NERVE_ID = "STIN_242"
    DEPARTMENT = "STIN"
    DIVISION = "pressure_mapping"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
