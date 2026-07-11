from infrastructure.nerve_base import NerveBase

class TSN_106_VoltageMonitoringNerve16(NerveBase):
    NERVE_ID = "TSN_106"
    DEPARTMENT = "TSN"
    DIVISION = "voltage_monitoring"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
