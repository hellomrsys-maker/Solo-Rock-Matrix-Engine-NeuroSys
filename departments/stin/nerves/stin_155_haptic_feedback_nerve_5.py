from infrastructure.nerve_base import NerveBase

class STIN_155_HapticFeedbackNerve5(NerveBase):
    NERVE_ID = "STIN_155"
    DEPARTMENT = "STIN"
    DIVISION = "haptic_feedback"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
