from infrastructure.nerve_base import NerveBase

class TSN_091_VoltageMonitoringNerve1(NerveBase):
    NERVE_ID = "TSN_091"
    DEPARTMENT = "TSN"
    DIVISION = "voltage_monitoring"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
