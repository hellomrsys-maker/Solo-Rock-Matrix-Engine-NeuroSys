from infrastructure.nerve_base import NerveBase

class CERN_080_ThreadDispatchNerve20(NerveBase):
    NERVE_ID = "CERN_080"
    DEPARTMENT = "CERN"
    DIVISION = "thread_dispatch"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
