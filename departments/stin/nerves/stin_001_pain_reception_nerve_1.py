from infrastructure.nerve_base import NerveBase
from infrastructure.event_bus import event_bus
from infrastructure.amsv import amsv_block

class STIN_001_PainReceptionNerve1(NerveBase):
    NERVE_ID = "STIN_001"
    DEPARTMENT = "STIN"
    DIVISION = "pain_reception"
    PIPELINE = "input" 
    WIRE_COLOR = "red"
    
    def __init__(self):
        super().__init__()
        # Subscribe explicitly to the physical hardware signal
        event_bus.subscribe("STIN_PHYSICAL_CLICK", self.fire)
    
    def fire(self):
        # Zero-Bridge: Read coordinates instantly from C-Memory
        super().fire()
        x = amsv_block.coord_x
        y = amsv_block.coord_y
        
        # Dispatch signal to visual renderer (No payload)
        event_bus.publish("PPVO_001")
