from infrastructure.nerve_base import NerveBase

class TSN_160_NetworkLatencyNerve10(NerveBase):
    NERVE_ID = "TSN_160"
    DEPARTMENT = "TSN"
    DIVISION = "network_latency"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
