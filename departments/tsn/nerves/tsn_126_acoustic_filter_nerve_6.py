from infrastructure.nerve_base import NerveBase

class TSN_126_AcousticFilterNerve6(NerveBase):
    NERVE_ID = "TSN_126"
    DEPARTMENT = "TSN"
    DIVISION = "acoustic_filter"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
