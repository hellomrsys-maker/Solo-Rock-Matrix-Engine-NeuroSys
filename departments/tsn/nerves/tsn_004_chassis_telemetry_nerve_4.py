from infrastructure.nerve_base import NerveBase

class TSN_004_ChassisTelemetryNerve4(NerveBase):
    NERVE_ID = "TSN_004"
    DEPARTMENT = "TSN"
    DIVISION = "chassis_telemetry"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
