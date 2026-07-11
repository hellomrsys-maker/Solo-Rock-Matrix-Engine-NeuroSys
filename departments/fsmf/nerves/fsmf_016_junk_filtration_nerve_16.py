from infrastructure.nerve_base import NerveBase

class FSMF_016_JunkFiltrationNerve16(NerveBase):
    NERVE_ID = "FSMF_016"
    DEPARTMENT = "FSMF"
    DIVISION = "junk_filtration"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
