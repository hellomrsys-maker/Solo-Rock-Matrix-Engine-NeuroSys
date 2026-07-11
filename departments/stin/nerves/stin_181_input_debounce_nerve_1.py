from infrastructure.nerve_base import NerveBase

class STIN_181_InputDebounceNerve1(NerveBase):
    NERVE_ID = "STIN_181"
    DEPARTMENT = "STIN"
    DIVISION = "input_debounce"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
