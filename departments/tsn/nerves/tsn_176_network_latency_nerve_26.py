from infrastructure.nerve_base import NerveBase

class TSN_176_NetworkLatencyNerve26(NerveBase):
    NERVE_ID = "TSN_176"
    DEPARTMENT = "TSN"
    DIVISION = "network_latency"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
