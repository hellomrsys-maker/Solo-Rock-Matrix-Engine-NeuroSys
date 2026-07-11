from infrastructure.nerve_base import NerveBase

class TSN_006_ChassisTelemetryNerve6(NerveBase):
    NERVE_ID = "TSN_006"
    DEPARTMENT = "TSN"
    DIVISION = "chassis_telemetry"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
