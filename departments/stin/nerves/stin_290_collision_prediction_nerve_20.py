from infrastructure.nerve_base import NerveBase

class STIN_290_CollisionPredictionNerve20(NerveBase):
    NERVE_ID = "STIN_290"
    DEPARTMENT = "STIN"
    DIVISION = "collision_prediction"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
