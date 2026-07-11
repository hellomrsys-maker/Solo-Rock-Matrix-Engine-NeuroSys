from infrastructure.nerve_base import NerveBase

class PPVO_080_DisplaySyncNerve20(NerveBase):
    NERVE_ID = "PPVO_080"
    DEPARTMENT = "PPVO"
    DIVISION = "display_sync"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
