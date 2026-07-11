import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall

class CAIN_046_GlialCellNerve46(NerveBase):
    NERVE_ID = "CAIN_046"
    DEPARTMENT = "CAIN"
    DIVISION = "glial_support"
    PIPELINE = "runtime"
    WIRE_COLOR = "teal"

    def __init__(self):
        super().__init__()
        self.glia_thread = threading.Thread(target=self._glia_loop, daemon=True)
        self.glia_thread.start()

    def fire(self): pass

    def _glia_loop(self):
        print("[CAIN_046] Glial Cell (Microglia) ACTIVE. Immune response online.")
        while True:
            my_ent = amsv_block.entities[46]
            
            # Immune System Regeneration: Spawn if dead
            if my_ent.health <= 0 or my_ent.z <= 0:
                my_ent.x = random.randint(1, 14) * 100.0
                my_ent.y = random.randint(1, 14) * 100.0
                my_ent.z = 200
                my_ent.health = 100
                
            # Scan for "Pathogens" (Player Bullets: Entities 1-10)
            target_bullet = None
            closest_dist = 99999.0
            
            for i in range(1, 11):
                bullet = amsv_block.entities[i]
                if bullet.z > 0:
                    dx = bullet.x - my_ent.x
                    dy = bullet.y - my_ent.y
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist < closest_dist:
                        closest_dist = dist
                        target_bullet = bullet
                        
            if target_bullet and closest_dist < 50.0:
                # Phagocytosis: Move towards pathogen to engulf it
                speed = 2.0
                dx = target_bullet.x - my_ent.x
                dy = target_bullet.y - my_ent.y
                
                new_x = my_ent.x + (dx / closest_dist) * speed
                new_y = my_ent.y + (dy / closest_dist) * speed
                if not is_wall(new_x, my_ent.y): my_ent.x = new_x
                if not is_wall(my_ent.x, new_y): my_ent.y = new_y
                
                # Engulf!
                if closest_dist < 5.0:
                    target_bullet.z = 0
                    my_ent.z = 0 # Glial cell sacrifices itself to destroy pathogen
            else:
                # Random wander (Patrolling)
                new_x = my_ent.x + random.uniform(-1.0, 1.0)
                new_y = my_ent.y + random.uniform(-1.0, 1.0)
                if not is_wall(new_x, my_ent.y): my_ent.x = new_x
                if not is_wall(my_ent.x, new_y): my_ent.y = new_y
                
            time.sleep(0.05)
