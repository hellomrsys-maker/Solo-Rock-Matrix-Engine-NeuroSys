import threading
import time
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class CAIN_035_InstructionRoutingNerve35(NerveBase):
    "\"\"
    PROJECTILE PHYSICS NERVE
    Controls Bullet 4. Moves it forward and checks AABB collision against Swarm.
    "\"\"
    NERVE_ID = "CAIN_035"
    DEPARTMENT = "CAIN"
    DIVISION = "instruction_routing"
    PIPELINE = "runtime"
    WIRE_COLOR = "purple"
    
    def __init__(self):
        super().__init__()
        self.entity_index = 4
        self.physics_thread = threading.Thread(target=self._physics_loop, daemon=True)
        self.physics_thread.start()

    def _check_aabb(self, x1, y1, z1, x2, y2, z2, size):
        return (abs(x1 - x2) < size and
                abs(y1 - y2) < size and
                abs(z1 - z2) < size)

    def _physics_loop(self):
        print("[CAIN_035] Projectile Node 4 ACTIVE.")
        
        while True:
            # 1. Zero-Bridge Read: My position
            mx = amsv_block.entities[self.entity_index].x
            my = amsv_block.entities[self.entity_index].y
            mz = amsv_block.entities[self.entity_index].z
            
            # If not spawned, sleep
            if mz == 0:
                time.sleep(0.016)
                continue
                
            # Move bullet forward aggressively
            mz += 50.0
            amsv_block.entities[self.entity_index].z = mz
            
            # Spin the bullet for visual flair
            amsv_block.entities[self.entity_index].rx += 0.2
            amsv_block.entities[self.entity_index].ry += 0.2
            
            # Despawn if it flies too far
            if mz > 4000.0:
                amsv_block.entities[self.entity_index].z = 0
                time.sleep(0.016)
                continue
                
            # Check collision against Swarm (Entities 61-90)
            # Swarm radius = 100, Bullet radius = 20
            hit_radius = 120.0
            
            for i in range(61, 91):
                sz = amsv_block.entities[i].z
                if sz == 0: continue
                
                sx = amsv_block.entities[i].x
                sy = amsv_block.entities[i].y
                
                if self._check_aabb(mx, my, mz, sx, sy, sz, hit_radius):
                    # HIT DETECTED!
                    # Destroy Bullet
                    amsv_block.entities[self.entity_index].z = 0
                    
                    # Destroy Swarm Enemy
                    amsv_block.entities[i].z = 0
                    
                    break # Stop checking other swarm enemies for this frame
            
            # Run at 60 FPS
            time.sleep(0.016)

    def fire(self): pass
