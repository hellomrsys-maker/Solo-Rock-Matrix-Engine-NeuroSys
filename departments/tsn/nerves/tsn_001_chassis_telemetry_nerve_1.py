from infrastructure.nerve_base import NerveBase

class TSN_001_ChassisTelemetryNerve1(NerveBase):
    NERVE_ID = "TSN_001"
    DEPARTMENT = "TSN"
    DIVISION = "chassis_telemetry"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
