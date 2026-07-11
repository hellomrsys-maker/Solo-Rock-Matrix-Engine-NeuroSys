import os

template = """import threading
import time
import math
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall

class CAIN_{NNN}_InstructionRoutingNerve{N}(NerveBase):
    \"\"\"
    SWARM AI NERVE {N} (With Pathfinding)
    Autonomous neural node designed to command Entity {N} and chase the Player, while respecting walls.
    \"\"\"
    NERVE_ID = "CAIN_{NNN}"
    DEPARTMENT = "CAIN"
    DIVISION = "instruction_routing"
    PIPELINE = "runtime"
    WIRE_COLOR = "purple"
    
    def __init__(self):
        super().__init__()
        self.entity_index = {N}
        self.physics_thread = threading.Thread(target=self._ai_loop, daemon=True)
        self.physics_thread.start()

    def _ai_loop(self):
        print(f"[CAIN_{NNN}] Swarm AI Node {N} ACTIVE (Pathfinding).")
        
        while True:
            # Determine which player is closer
            p1_hp = amsv_block.entities[0].health
            p2_hp = amsv_block.entities[200].health
            
            target_id = 0
            if p2_hp > 0 and p1_hp <= 0:
                target_id = 200
            elif p2_hp > 0 and p1_hp > 0:
                d1 = math.sqrt((amsv_block.entities[0].x - amsv_block.entities[self.entity_index].x)**2 + (amsv_block.entities[0].y - amsv_block.entities[self.entity_index].y)**2)
                d2 = math.sqrt((amsv_block.entities[200].x - amsv_block.entities[self.entity_index].x)**2 + (amsv_block.entities[200].y - amsv_block.entities[self.entity_index].y)**2)
                if d2 < d1: target_id = 200
                
            px = amsv_block.entities[target_id].x
            py = amsv_block.entities[target_id].y
            
            mx = amsv_block.entities[self.entity_index].x
            my = amsv_block.entities[self.entity_index].y
            mz = amsv_block.entities[self.entity_index].z
            
            if mz == 0:
                time.sleep(0.016)
                continue
                
            dx = px - mx
            dy = py - my
            
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 10:
                speed = 2.0
                move_x = (dx / distance) * speed
                move_y = (dy / distance) * speed
                
                # Check X slide
                if not is_wall(mx + move_x, my):
                    amsv_block.entities[self.entity_index].x += move_x
                
                # Check Y slide
                if not is_wall(mx, my + move_y):
                    amsv_block.entities[self.entity_index].y += move_y
                
                amsv_block.entities[self.entity_index].rx += 0.05
                amsv_block.entities[self.entity_index].ry += 0.05
            
            time.sleep(0.016)

    def fire(self): pass
"""

for i in range(61, 91):
    nnn = f"{i:03d}"
    content = template.replace("{NNN}", nnn).replace("{N}", str(i))
    filepath = f"departments/cain/nerves/cain_{nnn}_instruction_routing_nerve_{i}.py"
    with open(filepath, "w") as f:
        f.write(content)

print("Updated CAIN 61-90 with Swarm Pathfinding!")
