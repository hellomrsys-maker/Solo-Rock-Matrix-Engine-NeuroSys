import threading
import time
import math
import winsound
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class ALUS_061_AudioNerve61(NerveBase):
    "\"\"
    SPATIAL AUDIO NERVE 61
    Autonomous neural node designed to emit Doppler audio for Entity 61.
    "\"\"
    NERVE_ID = "ALUS_061"
    DEPARTMENT = "ALUS"
    DIVISION = "audio"
    PIPELINE = "runtime"
    WIRE_COLOR = "cyan"
    
    def __init__(self):
        super().__init__()
        self.entity_index = 61
        self.audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        self.audio_thread.start()

    def _audio_loop(self):
        print("[ALUS_061] Spatial Audio Node 61 ACTIVE.")
        
        while True:
            # 1. Zero-Bridge Read: Player position
            px = amsv_block.entities[0].x
            py = amsv_block.entities[0].y
            pz = amsv_block.entities[0].z
            
            # 2. Zero-Bridge Read: My position
            mx = amsv_block.entities[self.entity_index].x
            my = amsv_block.entities[self.entity_index].y
            mz = amsv_block.entities[self.entity_index].z
            
            # If the entity hasn't spawned yet, stay silent
            if mz == 0:
                time.sleep(0.016)
                continue
                
            # 3. Calculate 3D Distance
            dx = px - mx
            dy = py - my
            dz = pz - mz
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            # 4. Spatial Audio Trigger (Threat Radius = 600)
            if distance < 600:
                # The closer it is, the higher the pitch (up to ~1400Hz)
                freq = max(37, int(1500 - distance))
                
                try:
                    # Blocking audio call! This proves our thread isolation!
                    winsound.Beep(freq, 50)
                except Exception as e:
                    pass
                
                # Sleep a bit longer if it's far, rapid fire if close
                delay = max(0.05, distance / 2000.0)
                time.sleep(delay)
            else:
                # Outside threat radius, stay silent
                time.sleep(0.016)

    def fire(self): pass
