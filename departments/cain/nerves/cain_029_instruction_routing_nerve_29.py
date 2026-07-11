import threading
import time
import math
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class CAIN_029_InstructionRoutingNerve29(NerveBase):
    "\"\"
    COLLISION NERVE 29
    Autonomous neural node designed to calculate 3D AABB collisions for Swarm Entity 89.
    "\"\"
    NERVE_ID = "CAIN_029"
    DEPARTMENT = "CAIN"
    DIVISION = "instruction_routing"
    PIPELINE = "runtime"
    WIRE_COLOR = "purple"
    
    def __init__(self):
        super().__init__()
        self.entity_index = 89 # Corresponds to Swarm Entity 61-90
        self.physics_thread = threading.Thread(target=self._collision_loop, daemon=True)
        self.physics_thread.start()

    def _check_aabb(self, x1, y1, z1, x2, y2, z2, size):
        return (abs(x1 - x2) < size and
                abs(y1 - y2) < size and
                abs(z1 - z2) < size)

    def _collision_loop(self):
        print("[CAIN_029] 3D Collision Node 29 ACTIVE.")
        
        # Bounding box size (Cubes are drawn 50 units from center, so full width is 100)
        box_size = 100.0 
        
        while True:
            # 1. Zero-Bridge Read: My position
            mx = amsv_block.entities[self.entity_index].x
            my = amsv_block.entities[self.entity_index].y
            mz = amsv_block.entities[self.entity_index].z
            
            # If not spawned, sleep
            if mz == 0:
                time.sleep(0.016)
                continue
                
            # 2. Check collision against Player (Entity 0)
            px = amsv_block.entities[0].x
            py = amsv_block.entities[0].y
            pz = amsv_block.entities[0].z
            
            if self._check_aabb(mx, my, mz, px, py, pz, box_size):
                # Massive repulsion! Bounce away from player
                dx = mx - px
                dy = my - py
                dz = mz - pz
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                if dist == 0: dist = 0.001
                
                # Push back 20 units
                push = 20.0
                amsv_block.entities[self.entity_index].x += (dx / dist) * push
                amsv_block.entities[self.entity_index].y += (dy / dist) * push
                amsv_block.entities[self.entity_index].z += (dz / dist) * push
                
                # Damage the Player
                amsv_block.entities[0].health -= 10.0
                if amsv_block.entities[0].health < 0:
                    amsv_block.entities[0].health = 0
                
            # 3. Check collision against other Swarm Entities (61-90)
            for i in range(61, 91):
                if i == self.entity_index: continue
                
                ox = amsv_block.entities[i].x
                oy = amsv_block.entities[i].y
                oz = amsv_block.entities[i].z
                
                if oz == 0: continue
                
                if self._check_aabb(mx, my, mz, ox, oy, oz, box_size):
                    # Flocking repulsion! Push away from each other
                    dx = mx - ox
                    dy = my - oy
                    dz = mz - oz
                    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                    if dist == 0: dist = 0.001
                    
                    # Push back 5 units (softer bounce)
                    push = 5.0
                    amsv_block.entities[self.entity_index].x += (dx / dist) * push
                    amsv_block.entities[self.entity_index].y += (dy / dist) * push
                    amsv_block.entities[self.entity_index].z += (dz / dist) * push
            
            # Run Collision Checks at 60 FPS
            time.sleep(0.016)

    def fire(self): pass
