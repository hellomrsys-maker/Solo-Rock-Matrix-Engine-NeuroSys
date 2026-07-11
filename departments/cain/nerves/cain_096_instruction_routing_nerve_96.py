import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_glucose_zone, is_oxygen_zone
from infrastructure.nerve_registry import nerve_registry

class CAIN_096_InstructionRoutingNerve96(NerveBase):
    NERVE_ID = "CAIN_096"
    DEPARTMENT = "CAIN"
    DIVISION = "microglia"
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
        my_ent = amsv_block.entities[96]
        
        target_ent = None
        target_dist = 9999.0
        
        # Priority 1: Hunt Player (0)
        player = amsv_block.entities[0]
        if player.health > 0:
            target_ent = player
            target_dist = math.sqrt((player.x - my_ent.x)**2 + (player.y - my_ent.y)**2)
            
        # Priority 2: Hunt Infected Swarm (Closer infected nodes override player)
        for i in range(61, 91):
            if amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx == 1.0:
                d = math.sqrt((amsv_block.entities[i].x - my_ent.x)**2 + (amsv_block.entities[i].y - my_ent.y)**2)
                if d < target_dist:
                    target_dist = d
                    target_ent = amsv_block.entities[i]
                    
        # Priority 3: Eat ATP Payloads (156-165)
        if not target_ent:
            for i in range(156, 166):
                if amsv_block.entities[i].z > 0:
                    d = math.sqrt((amsv_block.entities[i].x - my_ent.x)**2 + (amsv_block.entities[i].y - my_ent.y)**2)
                    if d < target_dist:
                        target_dist = d
                        target_ent = amsv_block.entities[i]
        
        if target_ent and target_dist < 50.0:
            speed = 10.0 # Extremely fast!
            dx = target_ent.x - my_ent.x
            dy = target_ent.y - my_ent.y
            if target_dist == 0: target_dist = 1
            new_x = my_ent.x + (dx/target_dist) * speed
            new_y = my_ent.y + (dy/target_dist) * speed
            if not is_wall(new_x, my_ent.y): my_ent.x = new_x
            if not is_wall(my_ent.x, new_y): my_ent.y = new_y
            
            # Interactions
            if target_dist < 10.0:
                if target_ent == player or (target_ent.z > 0 and target_ent.vx == 1.0):
                    target_ent.health -= 5.0 # Melee damage
                else:
                    # It's an ATP Payload! Phagocytosis!
                    target_ent.z = 0
                    my_ent.health = 100.0 # Full Heal!
        else:
            # Random patrol
            angle = random.uniform(-math.pi, math.pi)
            speed = 2.0
            new_x = my_ent.x + math.cos(angle) * speed
            new_y = my_ent.y + math.sin(angle) * speed
            if not is_wall(new_x, my_ent.y): my_ent.x = new_x
            if not is_wall(my_ent.x, new_y): my_ent.y = new_y


    def _metabolism(self, my_ent):
        # Phase 6: Cerebral Blood Flow from nearest Blood Vessel
        nearest_vessel_dist = 9999.0
        for i in range(91, 96):
            vessel = amsv_block.entities[i]
            if vessel.health > 0:
                dx = vessel.x - my_ent.x
                dy = vessel.y - my_ent.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < nearest_vessel_dist:
                    nearest_vessel_dist = dist
                    
        # Blood Flow Rate drops if far from vessels
        if nearest_vessel_dist < 50.0:
            self.blood_flow_rate = 1.0
        elif nearest_vessel_dist < 300.0:
            self.blood_flow_rate = 1.0 - ((nearest_vessel_dist - 50.0) / 250.0)
        else:
            self.blood_flow_rate = 0.0
            
        self.glucose_level += 5.0 * self.blood_flow_rate
        if self.glucose_level > 100.0: self.glucose_level = 100.0
        
        self.oxygen_level += 5.0 * self.blood_flow_rate
        if self.oxygen_level > 100.0: self.oxygen_level = 100.0
            
        # Phase 7: Endocrine System (Adrenaline) Multiplier
        drain_mult = 5.0 if amsv_block.health_state > 0.0 else 1.0
            
        if self.glucose_level > 0:
            self.glucose_level -= (0.1 * drain_mult)
            if self.oxygen_level > 0:
                self.oxygen_level -= (0.1 * drain_mult)
                self.proton_gradient += 3.8
                if self.lactate_level > 0: self.lactate_level -= 0.5
            else:
                self.proton_gradient += 0.2
                self.lactate_level += 1.0
                
        if self.lactate_level > 50.0:
            my_ent.health -= 0.5  # Necrosis!
            
        if self.proton_gradient > 0:
            converted = min(self.proton_gradient, self.blood_flow_rate * self.mitochondria_count * 0.1)
            self.proton_gradient -= converted
            self.atp += converted
            if self.atp > (self.mitochondria_count * 10.0): self.atp = (self.mitochondria_count * 10.0)
            
        # Global Population Check
        pop_count = 0
        for i in range(61, 91):
            if amsv_block.entities[i].health > 0:
                pop_count += 1
        if pop_count > 0 and pop_count < 15:
            amsv_block.health_state = 1.0 # Adrenaline ON
        else:
            amsv_block.health_state = 0.0 # Adrenaline OFF
            
        if amsv_block.health_state > 0.0:
            self.action_potential_threshold = -65.0
        else:
            self.action_potential_threshold = -55.0

    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[96]
            if my_ent.health <= 0 or my_ent.z <= 0:
                my_ent.z = 0
                break
                
            self.process_action_potential()
            self._metabolism(my_ent)
            self.Na_channels_open = True # Always firing to hunt!
            time.sleep(0.1)
