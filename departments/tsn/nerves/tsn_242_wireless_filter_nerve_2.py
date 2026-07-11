from infrastructure.nerve_base import NerveBase

class TSN_242_WirelessFilterNerve2(NerveBase):
    NERVE_ID = "TSN_242"
    DEPARTMENT = "TSN"
    DIVISION = "wireless_filter"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
