from infrastructure.nerve_base import NerveBase

class STIN_122_GestureTrackingNerve2(NerveBase):
    NERVE_ID = "STIN_122"
    DEPARTMENT = "STIN"
    DIVISION = "gesture_tracking"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
