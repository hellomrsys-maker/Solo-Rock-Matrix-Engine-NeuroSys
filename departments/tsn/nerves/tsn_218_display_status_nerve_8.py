from infrastructure.nerve_base import NerveBase

class TSN_218_DisplayStatusNerve8(NerveBase):
    NERVE_ID = "TSN_218"
    DEPARTMENT = "TSN"
    DIVISION = "display_status"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
