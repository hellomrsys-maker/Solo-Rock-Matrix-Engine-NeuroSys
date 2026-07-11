from infrastructure.nerve_base import NerveBase

class STIN_182_InputDebounceNerve2(NerveBase):
    NERVE_ID = "STIN_182"
    DEPARTMENT = "STIN"
    DIVISION = "input_debounce"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
