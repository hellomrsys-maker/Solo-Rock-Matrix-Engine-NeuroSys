import os

common_imports = """import math
import random
import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_glucose_zone, is_oxygen_zone
from infrastructure.nerve_registry import nerve_registry
"""

metabolism_mixin = """
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
"""

# OCCIPITAL LOBE (Vision)
template_occipital = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
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
        my_ent = amsv_block.entities[{id}]
        if my_ent.vx == -1.0: return # Paralyzed!
        # When Occipital sees targets and fires AP, it excites Frontal and Temporal!
        for i in range(68, 76): # Frontal
            n = nerve_registry.get_nerve(f"CAIN_{i:03d}")
            if n: n.receive_neurotransmitter("EPSP", 15.0)
        for i in range(83, 91): # Temporal
            n = nerve_registry.get_nerve(f"CAIN_{i:03d}")
            if n: n.receive_neurotransmitter("EPSP", 10.0)

""" + metabolism_mixin + """
    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[{id}]
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
                    if i != {id} and amsv_block.entities[i].health > 0 and (amsv_block.entities[i].vx == 0.0 or i >= 96):
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
"""

# FRONTAL LOBE (Motor)
template_frontal = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
    DEPARTMENT = "CAIN"
    DIVISION = "frontal_lobe"
    PIPELINE = "runtime"
    WIRE_COLOR = "magenta"

    def __init__(self):
        super().__init__()
        self.action_potential_threshold = -55.0
        self.is_myelinated = True
        self.mitochondria_count = 20
        self.tonic_thread = threading.Thread(target=self._tonic_loop, daemon=True)
        self.tonic_thread.start()

    def fire(self):
        if self.atp < 20.0: return # Cellular Exhaustion Check
        self.atp -= 20.0
        
        my_ent = amsv_block.entities[{id}]
        if my_ent.vx == -1.0: return # Paralyzed!
        is_infected = (my_ent.vx == 1.0)
        
        target_ent = None
        target_dist = 9999.0
        
        if is_infected:
            # Hunt Microglia (96-98), T-Cells (131-135) and Uninfected Swarm
            targets = list(range(61, 99)) + list(range(131, 136))
            for i in targets:
                if i != {id} and amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx != 1.0:
                    ent = amsv_block.entities[i]
                    d = math.sqrt((ent.x - my_ent.x)**2 + (ent.y - my_ent.y)**2)
                    if d < target_dist:
                        target_dist = d
                        target_ent = ent
        else:
            # Hunt Player (0) and Infected Swarm
            target_ent = amsv_block.entities[0]
            target_dist = math.sqrt((target_ent.x - my_ent.x)**2 + (target_ent.y - my_ent.y)**2)
            if target_ent.health <= 0: target_dist = 9999.0
            
            for i in range(61, 91):
                if amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx == 1.0:
                    ent = amsv_block.entities[i]
                    d = math.sqrt((ent.x - my_ent.x)**2 + (ent.y - my_ent.y)**2)
                    if d < target_dist:
                        target_dist = d
                        target_ent = ent
                        
        if not target_ent or target_dist == 9999.0: return
        
        dx = target_ent.x - my_ent.x
        dy = target_ent.y - my_ent.y
        dist = target_dist
        if dist == 0: dist = 1
        
        # Fire Laser
        for i in range(100, 131):
            if amsv_block.entities[i].z <= 0:
                laser = amsv_block.entities[i]
                laser.x = my_ent.x
                laser.y = my_ent.y
                laser.z = 200
                laser.vx = (dx / dist) * 10.0
                laser.vy = (dy / dist) * 10.0
                break
                
        # Move (Double speed during Adrenaline!)
        speed = 6.0 if amsv_block.health_state > 0.0 else 3.0
        if abs(dx) > abs(dy):
            new_x = my_ent.x + (1.0 if dx > 0 else -1.0) * speed
            new_y = my_ent.y
        else:
            new_x = my_ent.x
            new_y = my_ent.y + (1.0 if dy > 0 else -1.0) * speed
            
        if not is_wall(new_x, my_ent.y): my_ent.x = new_x
        if not is_wall(my_ent.x, new_y): my_ent.y = new_y

""" + metabolism_mixin + """
    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[{id}]
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
                    break
                self.Na_channels_open = False # Paralyzed!
                time.sleep(0.1)
                continue
            
            # Phase 9: Viral Infection Check
            if my_ent.vx == 0.0 and amsv_block.entities[0].health > 0:
                dist_p = math.sqrt((my_ent.x - amsv_block.entities[0].x)**2 + (my_ent.y - amsv_block.entities[0].y)**2)
                if dist_p < 15.0:
                    my_ent.vx = 1.0 # INFECTED!
                    
            # Survival Instinct (Overrides Motor if starving)
            if self.glucose_level < 20.0 or self.oxygen_level < 20.0:
                self.Na_channels_open = True # Force movement
                speed = 6.0 if amsv_block.health_state > 0.0 else 3.0
                angle = random.uniform(-math.pi, math.pi)
                new_x = my_ent.x + math.cos(angle) * speed
                new_y = my_ent.y + math.sin(angle) * speed
                if not is_wall(new_x, my_ent.y): my_ent.x = new_x
                if not is_wall(my_ent.x, new_y): my_ent.y = new_y
            else:
                self.Na_channels_open = False # Only moves via EPSP
                
            time.sleep(0.1)
"""

# PARIETAL LOBE (Spatial)
template_parietal = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
    DEPARTMENT = "CAIN"
    DIVISION = "parietal_lobe"
    PIPELINE = "runtime"
    WIRE_COLOR = "magenta"

    def __init__(self):
        super().__init__()
        self.action_potential_threshold = -55.0
        self.is_myelinated = False
        self.mitochondria_count = 5
        self.tonic_thread = threading.Thread(target=self._tonic_loop, daemon=True)
        self.tonic_thread.start()

    def fire(self):
        pass # Parietal fires IPSPs in tonic loop, not here

""" + metabolism_mixin + """
    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[{id}]
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
                    break
                time.sleep(0.1)
                continue
                
            # Phase 9: Viral Infection Check
            if my_ent.vx == 0.0 and amsv_block.entities[0].health > 0:
                dist_p = math.sqrt((my_ent.x - amsv_block.entities[0].x)**2 + (my_ent.y - amsv_block.entities[0].y)**2)
                if dist_p < 15.0:
                    my_ent.vx = 1.0 # INFECTED!
                    
            # Check if Frontal nodes are near walls
            for i in range(68, 76):
                f_ent = amsv_block.entities[i]
                if f_ent.z > 0:
                    if is_wall(f_ent.x + 3.0, f_ent.y) or is_wall(f_ent.x - 3.0, f_ent.y) or is_wall(f_ent.x, f_ent.y + 3.0) or is_wall(f_ent.x, f_ent.y - 3.0):
                        n = nerve_registry.get_nerve(f"CAIN_{i:03d}")
                        if n: n.receive_neurotransmitter("IPSP", 2.0)
                        
            time.sleep(0.1)
"""

# TEMPORAL LOBE (Memory)
template_temporal = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
    DEPARTMENT = "CAIN"
    DIVISION = "temporal_lobe"
    PIPELINE = "runtime"
    WIRE_COLOR = "magenta"

    def __init__(self):
        super().__init__()
        self.action_potential_threshold = -55.0
        self.is_myelinated = False
        self.mitochondria_count = 10
        self.tonic_thread = threading.Thread(target=self._tonic_loop, daemon=True)
        self.tonic_thread.start()

    def fire(self):
        if self.atp < 5.0: return
        self.atp -= 5.0
        my_ent = amsv_block.entities[{id}]
        if my_ent.vx == -1.0: return
        # If Temporal hits AP, it sustains EPSP to Frontal
        for i in range(68, 76): # Frontal
            n = nerve_registry.get_nerve(f"CAIN_{i:03d}")
            if n: n.receive_neurotransmitter("EPSP", 5.0) # Keeps them moving!

""" + metabolism_mixin + """
    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[{id}]
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
                    break
                self.Na_channels_open = False
                time.sleep(0.1)
                continue
                
            # Phase 9: Viral Infection Check
            if my_ent.vx == 0.0 and amsv_block.entities[0].health > 0:
                dist_p = math.sqrt((my_ent.x - amsv_block.entities[0].x)**2 + (my_ent.y - amsv_block.entities[0].y)**2)
                if dist_p < 15.0:
                    my_ent.vx = 1.0 # INFECTED!
                    
            self.Na_channels_open = False
            time.sleep(0.1)
"""

# MICROGLIA (Immune System Hunter-Killers)
template_microglia = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
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
        my_ent = amsv_block.entities[{id}]
        
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

""" + metabolism_mixin + """
    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[{id}]
            if my_ent.health <= 0 or my_ent.z <= 0:
                my_ent.z = 0
                break
                
            self.process_action_potential()
            self._metabolism(my_ent)
            self.Na_channels_open = True # Always firing to hunt!
            time.sleep(0.1)
"""

# T-CELLS (Adaptive Immune System Hunter-Killers)
template_tcell = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
    DEPARTMENT = "CAIN"
    DIVISION = "tcell"
    PIPELINE = "runtime"
    WIRE_COLOR = "magenta"

    def __init__(self):
        super().__init__()
        self.action_potential_threshold = -55.0
        self.is_myelinated = True
        self.mitochondria_count = 15 # More energy!
        self.tonic_thread = threading.Thread(target=self._tonic_loop, daemon=True)
        self.tonic_thread.start()

    def fire(self):
        my_ent = amsv_block.entities[{id}]
        
        target_ent = None
        target_dist = 9999.0
        
        # T-Cells Hunt Player (0) and Infected Swarm (61-90)
        player = amsv_block.entities[0]
        if player.health > 0:
            target_ent = player
            target_dist = math.sqrt((player.x - my_ent.x)**2 + (player.y - my_ent.y)**2)
            
        for i in range(61, 91):
            if amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx == 1.0:
                d = math.sqrt((amsv_block.entities[i].x - my_ent.x)**2 + (amsv_block.entities[i].y - my_ent.y)**2)
                if d < target_dist:
                    target_dist = d
                    target_ent = amsv_block.entities[i]
        
        if target_ent and target_dist < 100.0:
            # Move towards target
            speed = 5.0
            dx = target_ent.x - my_ent.x
            dy = target_ent.y - my_ent.y
            if target_dist == 0: target_dist = 1
            new_x = my_ent.x + (dx/target_dist) * speed
            new_y = my_ent.y + (dy/target_dist) * speed
            if not is_wall(new_x, my_ent.y): my_ent.x = new_x
            if not is_wall(my_ent.x, new_y): my_ent.y = new_y
            
            # Fire Antibody!
            if random.random() < 0.2: # Limit firing rate
                for i in range(136, 151):
                    if amsv_block.entities[i].z <= 0:
                        antibody = amsv_block.entities[i]
                        antibody.x = my_ent.x
                        antibody.y = my_ent.y
                        antibody.z = 200 # Active
                        antibody_speed = 15.0
                        antibody.vx = (dx / target_dist) * antibody_speed
                        antibody.vy = (dy / target_dist) * antibody_speed
                        break
        else:
            # Random patrol
            angle = random.uniform(-math.pi, math.pi)
            speed = 3.0
            new_x = my_ent.x + math.cos(angle) * speed
            new_y = my_ent.y + math.sin(angle) * speed
            if not is_wall(new_x, my_ent.y): my_ent.x = new_x
            if not is_wall(my_ent.x, new_y): my_ent.y = new_y

""" + metabolism_mixin + """
    def _tonic_loop(self):
        while True:
            my_ent = amsv_block.entities[{id}]
            
            if my_ent.health <= 0:
                my_ent.z = 0 # Inactive
                
                # Check for Global Infection to respawn!
                infected_count = 0
                for i in range(61, 91):
                    if amsv_block.entities[i].health > 0 and amsv_block.entities[i].vx == 1.0:
                        infected_count += 1
                        
                if infected_count >= 5:
                    # Activate T-Cell!
                    my_ent.health = 100.0
                    my_ent.z = 100.0
                    # Spawn at random Blood Vessel
                    vessel = amsv_block.entities[random.randint(91, 95)]
                    my_ent.x = vessel.x
                    my_ent.y = vessel.y
                    print(f"[{id}] T-CELL DEPLOYED! INFECTION DETECTED.")
                
            else:
                self.process_action_potential()
                self._metabolism(my_ent)
                self.Na_channels_open = True # Always firing to hunt!
                
            time.sleep(0.1)
"""

# NEURAL STEM CELLS (Neurogenesis)
template_stemcell = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
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
        my_ent = amsv_block.entities[{id}]
        
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
                print(f"[{id}] STEM CELL DIFFERENTIATED INTO NODE {target_node}")
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
            my_ent = amsv_block.entities[{id}]
            
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
                    print(f"[{id}] STEM CELL DEPLOYED! REGENERATING NODE {dead_node}.")
                
            else:
                self.process_action_potential()
                self.Na_channels_open = True # Always firing to migrate!
                
            time.sleep(0.1)
"""

# ASTROCYTES (Blood-Brain Barrier)
template_astrocyte = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
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
        my_idx = {id}
        # Astrocytes are spawned 2 per blood vessel (91-95)
        # So vessel = 91 + (my_idx - 166) // 2
        vessel_idx = 91 + ((my_idx - 166) // 2)
        
        # Stagger the starting angle so they are on opposite sides
        offset = math.pi if (my_idx % 2 == 1) else 0.0
        
        while True:
            my_ent = amsv_block.entities[{id}]
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
"""

# MACROPHAGE (Final Boss Core - 176)
template_macrophage_core = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
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
            my_ent = amsv_block.entities[{id}]
            
            if my_ent.health <= 0:
                if boss_spawned:
                    key = amsv_block.entities[182]
                    if key.z == 0:
                        key.x = my_ent.x
                        key.y = my_ent.y
                        key.z = 1.0 # Active!
                        print(f"[{id}] MACROPHAGE DESTROYED! SOURCE CODE KEY DROPPED!")
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
                        print(f"[{id}] MACROPHAGE BOSS DEPLOYED! MASSIVE OUTBREAK DETECTED!")
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
                    print(f"[{id}] MACROPHAGE CYTOKINE STORM!")
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
"""

# MACROPHAGE (Final Boss Slaves - 177-179)
template_macrophage_slave = common_imports + """
class CAIN_{id_str}_InstructionRoutingNerve{id}(NerveBase):
    NERVE_ID = "CAIN_{id_str}"
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
        ox, oy = offsets[{id}]
        
        while True:
            core = amsv_block.entities[176]
            my_ent = amsv_block.entities[{id}]
            
            if core.health > 0:
                my_ent.health = core.health
                my_ent.z = core.z
                my_ent.x = core.x + ox
                my_ent.y = core.y + oy
            else:
                my_ent.z = 0
                my_ent.health = 0
                
            time.sleep(0.1)
"""

os.makedirs("departments/cain/nerves", exist_ok=True)
print("Generating Phase 13 AI (Macrophage Boss)...")
for i in range(61, 68):
    id_str = f"{i:03d}"
    content = template_occipital.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

for i in range(68, 76):
    id_str = f"{i:03d}"
    content = template_frontal.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)
        
for i in range(76, 83):
    id_str = f"{i:03d}"
    content = template_parietal.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

for i in range(83, 91):
    id_str = f"{i:03d}"
    content = template_temporal.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

for i in range(96, 99):
    id_str = f"{i:03d}"
    content = template_microglia.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

for i in range(131, 136):
    id_str = f"{i:03d}"
    content = template_tcell.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

for i in range(151, 156):
    id_str = f"{i:03d}"
    content = template_stemcell.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

for i in range(166, 176):
    id_str = f"{i:03d}"
    content = template_astrocyte.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

# Macrophage Core
content = template_macrophage_core.replace("{id_str}", "176").replace("{id}", "176")
with open(f"departments/cain/nerves/cain_176_instruction_routing_nerve_176.py", "w") as f:
    f.write(content)

# Macrophage Slaves
for i in range(177, 180):
    id_str = f"{i:03d}"
    content = template_macrophage_slave.replace("{id_str}", id_str).replace("{id}", str(i))
    with open(f"departments/cain/nerves/cain_{id_str}_instruction_routing_nerve_{i}.py", "w") as f:
        f.write(content)

print("Regenerated CAIN 061-098, 131-135, 151-155, 166-175, and 176-179! (Macrophage Boss Edition)")
