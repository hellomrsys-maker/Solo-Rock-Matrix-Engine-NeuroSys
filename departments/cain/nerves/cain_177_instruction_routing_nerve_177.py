import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_glucose_zone, is_oxygen_zone
from infrastructure.nerve_registry import nerve_registry

class CAIN_177_InstructionRoutingNerve177(NerveBase):
    NERVE_ID = "CAIN_177"
    DEPARTMENT = "CAIN"
    DIVISION = "macrophage_slave"
    PIPELINE = "runtime"
    WIRE_COLOR = "magenta"

    def __init__(self):
        super().__init__()
        self.action_potential_threshold = -55.0
        self.is_myelinated = True
        self.mitochondria_count = 1
        self.tonic_thread = threading.Thread(target=self._tonic_loop, daemon=True)
        self.tonic_thread.start()

    def fire(self):
        pass

    def _tonic_loop(self):
        offsets = {
            177: (-20.0, -20.0),
            178: (20.0, -20.0),
            179: (0.0, 20.0)
        }
        ox, oy = offsets[177]
        
        while True:
            core = amsv_block.entities[176]
            my_ent = amsv_block.entities[177]
            
            if core.health > 0:
                my_ent.health = core.health
                my_ent.z = core.z
                my_ent.x = core.x + ox
                my_ent.y = core.y + oy
            else:
                my_ent.z = 0
                my_ent.health = 0
                
            time.sleep(0.1)
