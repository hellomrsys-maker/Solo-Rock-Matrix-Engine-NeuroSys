from infrastructure.nerve_base import NerveBase

class PPVO_020_PhysicsPredictionNerve20(NerveBase):
    NERVE_ID = "PPVO_020"
    DEPARTMENT = "PPVO"
    DIVISION = "physics_prediction"
    PIPELINE = "runtime" # Default, to be customized
    WIRE_COLOR = "teal" # Default, to be customized
    
    def fire(self, payload):
        pass
