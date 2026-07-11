from infrastructure.nerve_base import NerveBase

class STIN_020_PainReceptionNerve20(NerveBase):
    NERVE_ID = "STIN_020"
    DEPARTMENT = "STIN"
    DIVISION = "pain_reception"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
