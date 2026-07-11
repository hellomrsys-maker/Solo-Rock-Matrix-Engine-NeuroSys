import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_glucose_zone, is_oxygen_zone
from infrastructure.nerve_registry import nerve_registry

class CAIN_152_InstructionRoutingNerve152(NerveBase):
    NERVE_ID = "CAIN_152"
    DEPARTMENT = "CAIN"
    DIVISION = "stemcell"
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
        my_ent = amsv_block.entities[152]
        
        target_node = int(my_ent.rz)
        if target_node >= 61 and target_node <= 90:
            target_ent = amsv_block.entities[target_node]
            dx = target_ent.x - my_ent.x
            dy = target_ent.y - my_ent.y
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist < 10.0:
                # DIFFERENTIATION (Revive the Node)
                target_ent.health = 100.0
                target_ent.z = 50.0
                target_ent.vx = 0.0 # Clean
                target_ent.rz = 0.0
                my_ent.health = 0.0 # Stem Cell dies (becomes the new node)
                my_ent.z = 0.0
                print(f"[152] STEM CELL DIFFERENTIATED INTO NODE {target_node}")
            else:
                # Migrate towards damaged area
                speed = 4.0
                if dist == 0: dist = 1
                new_x = my_ent.x + (dx/dist) * speed
                new_y = my_ent.y + (dy/dist) * speed
                if not is_wall(new_x, my_ent.y): my_ent.x = new_x
                if not is_wall(my_ent.x, new_y): my_ent.y = new_y

    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[152]
            
            if my_ent.health <= 0:
                my_ent.z = 0 # Inactive
                
                # Check for dead nodes to replace
                dead_node = -1
                for i in range(61, 91):
                    if amsv_block.entities[i].health <= 0:
                        dead_node = i
                        break
                        
                if dead_node != -1:
                    # Activate Stem Cell!
                    my_ent.health = 100.0
                    my_ent.z = 100.0
                    my_ent.x = 0.0 # Hippocampus
                    my_ent.y = 0.0
                    my_ent.rz = float(dead_node)
                    print(f"[152] STEM CELL DEPLOYED! REGENERATING NODE {dead_node}.")
                
            else:
                self.process_action_potential()
                self.Na_channels_open = True # Always firing to migrate!
                
            time.sleep(0.1)
