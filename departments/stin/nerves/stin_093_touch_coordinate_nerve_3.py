from infrastructure.nerve_base import NerveBase

class STIN_093_TouchCoordinateNerve3(NerveBase):
    NERVE_ID = "STIN_093"
    DEPARTMENT = "STIN"
    DIVISION = "touch_coordinate"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
