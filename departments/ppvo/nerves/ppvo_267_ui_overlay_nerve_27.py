from infrastructure.nerve_base import NerveBase

class PPVO_267_UiOverlayNerve27(NerveBase):
    NERVE_ID = "PPVO_267"
    DEPARTMENT = "PPVO"
    DIVISION = "ui_overlay"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
