from infrastructure.nerve_base import NerveBase

class STIN_271_CollisionPredictionNerve1(NerveBase):
    NERVE_ID = "STIN_271"
    DEPARTMENT = "STIN"
    DIVISION = "collision_prediction"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
