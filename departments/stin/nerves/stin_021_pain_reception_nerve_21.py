from infrastructure.nerve_base import NerveBase

class STIN_021_PainReceptionNerve21(NerveBase):
    NERVE_ID = "STIN_021"
    DEPARTMENT = "STIN"
    DIVISION = "pain_reception"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
