from infrastructure.nerve_base import NerveBase

class STIN_210_InputDebounceNerve30(NerveBase):
    NERVE_ID = "STIN_210"
    DEPARTMENT = "STIN"
    DIVISION = "input_debounce"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
