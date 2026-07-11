from infrastructure.nerve_base import NerveBase

class CAIN_211_RegisterPipelineNerve1(NerveBase):
    NERVE_ID = "CAIN_211"
    DEPARTMENT = "CAIN"
    DIVISION = "register_pipeline"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
