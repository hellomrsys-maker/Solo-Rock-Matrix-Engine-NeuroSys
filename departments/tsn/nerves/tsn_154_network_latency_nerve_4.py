from infrastructure.nerve_base import NerveBase

class TSN_154_NetworkLatencyNerve4(NerveBase):
    NERVE_ID = "TSN_154"
    DEPARTMENT = "TSN"
    DIVISION = "network_latency"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
