from infrastructure.nerve_base import NerveBase

class PPVO_121_TextureStreamingNerve1(NerveBase):
    NERVE_ID = "PPVO_121"
    DEPARTMENT = "PPVO"
    DIVISION = "texture_streaming"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
