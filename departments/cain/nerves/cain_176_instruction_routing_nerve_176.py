import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_glucose_zone, is_oxygen_zone
from infrastructure.nerve_registry import nerve_registry

class CAIN_176_InstructionRoutingNerve176(NerveBase):
    NERVE_ID = "CAIN_176"
    DEPARTMENT = "CAIN"
    DIVISION = "macrophage_core"
    PIPELINE = "runtime"
    WIRE_COLOR = "magenta"

    def __init__(self):
        super().__init__()
        self.action_potential_threshold = -55.0
        self.is_myelinated = True
        self.mitochondria_count = 50 # Boss energy!
        self.tonic_thread = threading.Thread(target=self._tonic_loop, daemon=True)
        self.tonic_thread.start()

    def fire(self):
        pass # Only uses tonic loop

    def _tonic_loop(self):
        boss_spawned = False
        while True:
            my_ent = amsv_block.entities[176]
            
            if my_ent.health <= 0:
                if boss_spawned:
                    key = amsv_block.entities[182]
                    if key.z == 0:
                        key.x = my_ent.x
                        key.y = my_ent.y
                        key.z = 1.0 # Active!
                        print(f"[176] MACROPHAGE DESTROYED! SOURCE CODE KEY DROPPED!")
                        boss_spawned = False
                        
                my_ent.z = 0
                if not boss_spawned and amsv_block.entities[182].z == 0:
                    # Check for massive outbreak
                    infected_count = 0
                    for i in range(61, 91):
                        if amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx == 1.0:
                            infected_count += 1
                            
                    if infected_count >= 15:
                        # SPAWN BOSS!
                        boss_spawned = True
                        my_ent.health = 1500.0 # Huge Health Pool!
                        my_ent.z = 100.0
                        my_ent.x = 0.0
                        my_ent.y = 0.0
                        print(f"[176] MACROPHAGE BOSS DEPLOYED! MASSIVE OUTBREAK DETECTED!")
            else:
                # BOSS AI
                target_ent = None
                target_dist = 9999.0
                
                # Priorities: Eat Infected Nodes, Hunt Player
                for i in range(61, 91):
                    if amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx == 1.0:
                        d = math.sqrt((amsv_block.entities[i].x - my_ent.x)**2 + (amsv_block.entities[i].y - my_ent.y)**2)
                        if d < target_dist:
                            target_dist = d
                            target_ent = amsv_block.entities[i]
                            
                player = amsv_block.entities[0]
                if player.health > 0:
                    d = math.sqrt((player.x - my_ent.x)**2 + (player.y - my_ent.y)**2)
                    if d < target_dist:
                        target_dist = d
                        target_ent = player
                        
                if target_ent:
                    speed = 2.0 # Slow moving behemoth
                    dx = target_ent.x - my_ent.x
                    dy = target_ent.y - my_ent.y
                    if target_dist == 0: target_dist = 1
                    
                    new_x = my_ent.x + (dx/target_dist) * speed
                    new_y = my_ent.y + (dy/target_dist) * speed
                    # Boss ignores walls (phases through tissue)
                    my_ent.x = new_x
                    my_ent.y = new_y
                    
                    # Phagocytosis!
                    if target_dist < 40.0: # Huge reach
                        if target_ent == player:
                            player.health -= 10.0 # Huge damage
                        else:
                            # Eat the infected node
                            target_ent.health = 0.0
                            target_ent.vx = 0.0
                            my_ent.health += 50.0 # Heal boss!
                            if my_ent.health > 1500.0: my_ent.health = 1500.0
                            
                # Cytokine Storm Check
                if my_ent.health < 500.0 and random.random() < 0.05:
                    print(f"[176] MACROPHAGE CYTOKINE STORM!")
                    angle = 0
                    for i in range(136, 151): # 15 Antibodies
                        if amsv_block.entities[i].z <= 0:
                            antibody = amsv_block.entities[i]
                            antibody.x = my_ent.x
                            antibody.y = my_ent.y
                            antibody.z = 200
                            antibody_speed = 10.0
                            antibody.vx = math.cos(angle) * antibody_speed
                            antibody.vy = math.sin(angle) * antibody_speed
                        angle += (math.pi * 2) / 15.0
                        
            time.sleep(0.1)
