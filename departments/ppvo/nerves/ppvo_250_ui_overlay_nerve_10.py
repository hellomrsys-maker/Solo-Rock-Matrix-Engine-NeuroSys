from infrastructure.nerve_base import NerveBase

class PPVO_250_UiOverlayNerve10(NerveBase):
    NERVE_ID = "PPVO_250"
    DEPARTMENT = "PPVO"
    DIVISION = "ui_overlay"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
