from infrastructure.nerve_base import NerveBase

class CERN_058_CacheControlNerve28(NerveBase):
    NERVE_ID = "CERN_058"
    DEPARTMENT = "CERN"
    DIVISION = "cache_control"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
