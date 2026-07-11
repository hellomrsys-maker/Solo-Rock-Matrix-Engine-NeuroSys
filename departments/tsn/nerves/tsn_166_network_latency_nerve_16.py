from infrastructure.nerve_base import NerveBase

class TSN_166_NetworkLatencyNerve16(NerveBase):
    NERVE_ID = "TSN_166"
    DEPARTMENT = "TSN"
    DIVISION = "network_latency"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
