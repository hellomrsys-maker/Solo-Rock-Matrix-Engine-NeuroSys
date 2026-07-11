from infrastructure.nerve_base import NerveBase

class STIN_018_PainReceptionNerve18(NerveBase):
    NERVE_ID = "STIN_018"
    DEPARTMENT = "STIN"
    DIVISION = "pain_reception"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
