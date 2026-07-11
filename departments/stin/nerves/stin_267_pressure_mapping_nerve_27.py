from infrastructure.nerve_base import NerveBase

class STIN_267_PressureMappingNerve27(NerveBase):
    NERVE_ID = "STIN_267"
    DEPARTMENT = "STIN"
    DIVISION = "pressure_mapping"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
