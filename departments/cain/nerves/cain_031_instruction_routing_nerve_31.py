import threading
import time
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class CAIN_031_InstructionRoutingNerve31(NerveBase):
    """
    WEAPON TRIGGER NERVE
    Monitors Left Mouse Click. Spawns projectiles in Entity Slots 1-10.
    """
    NERVE_ID = "CAIN_031"
    DEPARTMENT = "CAIN"
    DIVISION = "instruction_routing"
    PIPELINE = "runtime"
    WIRE_COLOR = "purple"
    
    def __init__(self):
        super().__init__()
        self.trigger_thread = threading.Thread(target=self._trigger_loop, daemon=True)
        self.trigger_thread.start()

    def _trigger_loop(self):
        print("[CAIN_031] Weapon Trigger Node ACTIVE.")
        
        LEFT_CLICK_BIT = 1 << 0
        cooldown = 0
        
        while True:
            # Cooldown management
            if cooldown > 0:
                cooldown -= 1
                
            # If left click is pressed and not on cooldown
            if (amsv_block.mouse_state & LEFT_CLICK_BIT) and cooldown == 0:
                # Find an available projectile slot (Entities 1 to 10)
                for i in range(1, 11):
                    # Z == 0 means it is despawned / inactive
                    if amsv_block.entities[i].z == 0:
                        # Spawn bullet slightly in front of the player
                        amsv_block.entities[i].x = amsv_block.entities[0].x
                        amsv_block.entities[i].y = amsv_block.entities[0].y
                        amsv_block.entities[i].z = amsv_block.entities[0].z + 100.0
                        
                        # Reset rotation
                        amsv_block.entities[i].rx = 0.0
                        amsv_block.entities[i].ry = 0.0
                        amsv_block.entities[i].rz = 0.0
                        
                        # Set a 15-frame cooldown (~250ms fire rate)
                        cooldown = 15
                        break # Only shoot one bullet per click
            
            # Run at 60 FPS
            time.sleep(0.016)

    def fire(self): pass
