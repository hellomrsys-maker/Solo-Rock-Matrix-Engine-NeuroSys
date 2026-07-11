from infrastructure.nerve_base import NerveBase

class STIN_080_PumpExecutionNerve20(NerveBase):
    NERVE_ID = "STIN_080"
    DEPARTMENT = "STIN"
    DIVISION = "pump_execution"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
