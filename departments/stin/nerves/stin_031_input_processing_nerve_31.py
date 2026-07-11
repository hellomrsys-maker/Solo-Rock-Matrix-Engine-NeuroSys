import threading
import time
import random
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class STIN_031_InputProcessingNerve31(NerveBase):
    """
    GAME DIRECTOR NERVE
    Monitors Swarm states. Spawns new waves when Swarm is eradicated. Manages initial Player Health.
    """
    NERVE_ID = "STIN_031"
    DEPARTMENT = "STIN"
    DIVISION = "input_processing"
    PIPELINE = "input"
    WIRE_COLOR = "green"
    
    def __init__(self):
        super().__init__()
        self.director_thread = threading.Thread(target=self._director_loop, daemon=True)
        self.director_thread.start()

    def _director_loop(self):
        print("[STIN_031] Game Director Node ACTIVE.")
        
        # Initialize Player Health
        if amsv_block.entities[0].health == 0:
            amsv_block.entities[0].health = 100.0
            
        wave_number = 1
        
        while True:
            # Prevent wave logic from running during Time Reversal
            SPACEBAR_BIT = 1 << 4
            if amsv_block.keyboard_state & SPACEBAR_BIT:
                time.sleep(0.016)
                continue
                
            # Check if all Swarm entities are destroyed
            swarm_alive = False
            for i in range(61, 91):
                if amsv_block.entities[i].z > 0:
                    swarm_alive = True
                    break
                    
            if not swarm_alive:
                wave_number += 1
                print(f"[DIRECTOR] Swarm Eradicated. Spawning WAVE {wave_number}!")
                
                # Spawn new wave
                for i in range(61, 91):
                    amsv_block.entities[i].x = random.uniform(-1500, 1500)
                    amsv_block.entities[i].y = random.uniform(-1500, 1500)
                    amsv_block.entities[i].z = random.uniform(1500, 3000)
                    amsv_block.entities[i].rx = random.uniform(0, 3.14)
                    amsv_block.entities[i].ry = random.uniform(0, 3.14)
                    
            # Run at 2 FPS (Director doesn't need to run at 60 FPS)
            time.sleep(0.5)

    def fire(self): pass
