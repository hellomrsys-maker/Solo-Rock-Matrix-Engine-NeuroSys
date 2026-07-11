from infrastructure.nerve_base import NerveBase

class TSN_152_NetworkLatencyNerve2(NerveBase):
    NERVE_ID = "TSN_152"
    DEPARTMENT = "TSN"
    DIVISION = "network_latency"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
