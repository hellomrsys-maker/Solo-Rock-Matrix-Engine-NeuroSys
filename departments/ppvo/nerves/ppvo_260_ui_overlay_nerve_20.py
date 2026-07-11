from infrastructure.nerve_base import NerveBase

class PPVO_260_UiOverlayNerve20(NerveBase):
    NERVE_ID = "PPVO_260"
    DEPARTMENT = "PPVO"
    DIVISION = "ui_overlay"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
