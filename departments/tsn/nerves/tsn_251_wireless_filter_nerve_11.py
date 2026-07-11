from infrastructure.nerve_base import NerveBase

class TSN_251_WirelessFilterNerve11(NerveBase):
    NERVE_ID = "TSN_251"
    DEPARTMENT = "TSN"
    DIVISION = "wireless_filter"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
