from infrastructure.nerve_base import NerveBase

class PPVO_135_TextureStreamingNerve15(NerveBase):
    NERVE_ID = "PPVO_135"
    DEPARTMENT = "PPVO"
    DIVISION = "texture_streaming"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
