from infrastructure.nerve_base import NerveBase

class STIN_152_HapticFeedbackNerve2(NerveBase):
    NERVE_ID = "STIN_152"
    DEPARTMENT = "STIN"
    DIVISION = "haptic_feedback"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
