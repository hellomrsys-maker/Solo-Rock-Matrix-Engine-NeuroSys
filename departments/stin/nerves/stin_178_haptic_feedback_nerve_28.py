from infrastructure.nerve_base import NerveBase

class STIN_178_HapticFeedbackNerve28(NerveBase):
    NERVE_ID = "STIN_178"
    DEPARTMENT = "STIN"
    DIVISION = "haptic_feedback"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
