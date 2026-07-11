from infrastructure.nerve_base import NerveBase

class CERN_036_CacheControlNerve6(NerveBase):
    NERVE_ID = "CERN_036"
    DEPARTMENT = "CERN"
    DIVISION = "cache_control"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
