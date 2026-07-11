import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_glucose_zone, is_oxygen_zone
from infrastructure.nerve_registry import nerve_registry

class CAIN_167_InstructionRoutingNerve167(NerveBase):
    NERVE_ID = "CAIN_167"
    DEPARTMENT = "CAIN"
    DIVISION = "astrocyte"
    PIPELINE = "runtime"
    WIRE_COLOR = "magenta"

    def __init__(self):
        super().__init__()
        self.action_potential_threshold = -55.0
        self.is_myelinated = True
        self.mitochondria_count = 10
        self.tonic_thread = threading.Thread(target=self._tonic_loop, daemon=True)
        self.tonic_thread.start()

    def fire(self):
        pass # Only uses tonic loop for kinetic shielding

    def _tonic_loop(self):
        # 166-175
        my_idx = 167
        # Astrocytes are spawned 2 per blood vessel (91-95)
        # So vessel = 91 + (my_idx - 166) // 2
        vessel_idx = 91 + ((my_idx - 166) // 2)
        
        # Stagger the starting angle so they are on opposite sides
        offset = math.pi if (my_idx % 2 == 1) else 0.0
        
        while True:
            my_ent = amsv_block.entities[167]
            if my_ent.health <= 0 or my_ent.z <= 0:
                break
                
            vessel = amsv_block.entities[vessel_idx]
            
            # Astrocytes are physically attached to the vessel, so they heal rapidly!
            if vessel.health > 0 and my_ent.health < 200.0:
                my_ent.health += 5.0
                
            # Orbital Kinetic Shield Mechanics
            my_ent.rz += 0.5 # Fast spin!
            orbit_radius = 45.0
            
            my_ent.x = vessel.x + math.cos(my_ent.rz + offset) * orbit_radius
            my_ent.y = vessel.y + math.sin(my_ent.rz + offset) * orbit_radius
            
            time.sleep(0.05)
