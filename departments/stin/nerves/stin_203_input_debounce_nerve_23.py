from infrastructure.nerve_base import NerveBase

class STIN_203_InputDebounceNerve23(NerveBase):
    NERVE_ID = "STIN_203"
    DEPARTMENT = "STIN"
    DIVISION = "input_debounce"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
