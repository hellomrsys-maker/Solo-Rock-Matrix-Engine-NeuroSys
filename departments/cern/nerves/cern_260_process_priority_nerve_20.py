from infrastructure.nerve_base import NerveBase

class CERN_260_ProcessPriorityNerve20(NerveBase):
    NERVE_ID = "CERN_260"
    DEPARTMENT = "CERN"
    DIVISION = "process_priority"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
