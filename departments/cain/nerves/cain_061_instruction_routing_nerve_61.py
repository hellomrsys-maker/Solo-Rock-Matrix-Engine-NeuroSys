import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_glucose_zone, is_oxygen_zone
from infrastructure.nerve_registry import nerve_registry

class CAIN_061_InstructionRoutingNerve61(NerveBase):
    NERVE_ID = "CAIN_061"
    DEPARTMENT = "CAIN"
    DIVISION = "occipital_lobe"
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
        if self.atp < 10.0: return
        self.atp -= 10.0
        my_ent = amsv_block.entities[61]
        if my_ent.vx == -1.0: return # Paralyzed!
        # When Occipital sees targets and fires AP, it excites Frontal and Temporal!
        for i in range(68, 76): # Frontal
            n = nerve_registry.get_nerve(f"CAIN_{i:03d}")
            if n: n.receive_neurotransmitter("EPSP", 15.0)
        for i in range(83, 91): # Temporal
            n = nerve_registry.get_nerve(f"CAIN_{i:03d}")
            if n: n.receive_neurotransmitter("EPSP", 10.0)


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
            my_ent = amsv_block.entities[61]
            if my_ent.health <= 0:
                if my_ent.z > 0:
                    my_ent.z = 0
                    amsv_block.ai_target_x = my_ent.x
                    amsv_block.ai_target_y = my_ent.y
                break
                
            self.process_action_potential()
            self._metabolism(my_ent)
            
            # Phase 11: Apoptosis
            if my_ent.vx == -1.0 or my_ent.health <= 0:
                my_ent.rz += 1
                if my_ent.rz > 50:
                    my_ent.health = 0 # Die!
                    my_ent.vx = 0
                    my_ent.rz = 0
                    # Drop ATP Payload
                    for k in range(156, 166):
                        if amsv_block.entities[k].z <= 0:
                            amsv_block.entities[k].x = my_ent.x
                            amsv_block.entities[k].y = my_ent.y
                            amsv_block.entities[k].z = 100
                            amsv_block.entities[k].health = 100
                            break
                    break # exit loop since we are dead
                self.Na_channels_open = False # Paralyzed!
                time.sleep(0.1)
                continue
            
            # Phase 9: Viral Infection Check
            if my_ent.vx == 0.0 and amsv_block.entities[0].health > 0:
                dist_p = math.sqrt((my_ent.x - amsv_block.entities[0].x)**2 + (my_ent.y - amsv_block.entities[0].y)**2)
                if dist_p < 15.0:
                    my_ent.vx = 1.0 # INFECTED!
                
            # Occipital Vision
            target_found = False
            if my_ent.vx == 1.0:
                # Infected: Look for Microglia or Uninfected Swarm
                for i in range(61, 99):
                    if i != 61 and amsv_block.entities[i].health > 0 and (amsv_block.entities[i].vx == 0.0 or i >= 96):
                        dist = math.sqrt((my_ent.x - amsv_block.entities[i].x)**2 + (my_ent.y - amsv_block.entities[i].y)**2)
                        if dist < 40.0:
                            target_found = True
                            break
            else:
                # Uninfected: Look for Player or Infected Swarm
                player = amsv_block.entities[0]
                if player.health > 0:
                    dist = math.sqrt((player.x - my_ent.x)**2 + (player.y - my_ent.y)**2)
                    if dist < 40.0: target_found = True
                if not target_found:
                    for i in range(61, 91):
                        if amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx == 1.0:
                            dist = math.sqrt((my_ent.x - amsv_block.entities[i].x)**2 + (my_ent.y - amsv_block.entities[i].y)**2)
                            if dist < 40.0:
                                target_found = True
                                break
                                
            if target_found and self.ap_state != "UNDERSHOOT":
                self.Na_channels_open = True
            else:
                self.Na_channels_open = False
                
            time.sleep(0.1)
