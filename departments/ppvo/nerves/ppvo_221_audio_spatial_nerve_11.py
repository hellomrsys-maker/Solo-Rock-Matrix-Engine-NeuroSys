from infrastructure.nerve_base import NerveBase

class PPVO_221_AudioSpatialNerve11(NerveBase):
    NERVE_ID = "PPVO_221"
    DEPARTMENT = "PPVO"
    DIVISION = "audio_spatial"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
