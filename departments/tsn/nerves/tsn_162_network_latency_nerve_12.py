from infrastructure.nerve_base import NerveBase

class TSN_162_NetworkLatencyNerve12(NerveBase):
    NERVE_ID = "TSN_162"
    DEPARTMENT = "TSN"
    DIVISION = "network_latency"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
