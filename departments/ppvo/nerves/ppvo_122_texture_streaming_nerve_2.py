from infrastructure.nerve_base import NerveBase

class PPVO_122_TextureStreamingNerve2(NerveBase):
    NERVE_ID = "PPVO_122"
    DEPARTMENT = "PPVO"
    DIVISION = "texture_streaming"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
