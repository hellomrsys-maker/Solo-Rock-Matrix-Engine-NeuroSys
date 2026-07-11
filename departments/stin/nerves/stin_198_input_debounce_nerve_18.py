from infrastructure.nerve_base import NerveBase

class STIN_198_InputDebounceNerve18(NerveBase):
    NERVE_ID = "STIN_198"
    DEPARTMENT = "STIN"
    DIVISION = "input_debounce"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
