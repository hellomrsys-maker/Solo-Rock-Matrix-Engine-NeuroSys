from infrastructure.nerve_base import NerveBase

class TSN_177_NetworkLatencyNerve27(NerveBase):
    NERVE_ID = "TSN_177"
    DEPARTMENT = "TSN"
    DIVISION = "network_latency"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
