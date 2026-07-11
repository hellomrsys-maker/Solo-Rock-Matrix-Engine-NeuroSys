from infrastructure.nerve_base import NerveBase

class FSMF_004_JunkFiltrationNerve4(NerveBase):
    NERVE_ID = "FSMF_004"
    DEPARTMENT = "FSMF"
    DIVISION = "junk_filtration"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
