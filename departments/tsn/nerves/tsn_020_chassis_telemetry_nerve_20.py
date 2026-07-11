from infrastructure.nerve_base import NerveBase

class TSN_020_ChassisTelemetryNerve20(NerveBase):
    NERVE_ID = "TSN_020"
    DEPARTMENT = "TSN"
    DIVISION = "chassis_telemetry"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
