import threading
import time
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class ALUS_132_AudioSpatialNerve2(NerveBase):
    """
    DAMAGE AUDIO NERVE
    Monitors player health and generates retro 8-bit hit markers.
    """
    NERVE_ID = "ALUS_132"
    DEPARTMENT = "ALUS"
    DIVISION = "audio_spatial"
    PIPELINE = "runtime"
    WIRE_COLOR = "cyan"
    
    def __init__(self):
        super().__init__()
        self.audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        self.audio_thread.start()

    def _play_hit(self):
        import winsound
        winsound.Beep(150, 100) # Deep thud
        winsound.Beep(100, 150)

    def _audio_loop(self):
        print("[ALUS_132] Damage Audio Node ACTIVE (8-bit Mode).")
        
        last_hp_p1 = 100.0
        last_hp_p2 = 100.0
        
        # Wait a moment for things to spawn
        time.sleep(2)
        
        while True:
            hp_p1 = amsv_block.entities[0].health
            hp_p2 = amsv_block.entities[200].health
            
            if hp_p1 < last_hp_p1 and hp_p1 > 0:
                threading.Thread(target=self._play_hit, daemon=True).start()
                
            if hp_p2 < last_hp_p2 and hp_p2 > 0:
                threading.Thread(target=self._play_hit, daemon=True).start()
                
            last_hp_p1 = hp_p1
            last_hp_p2 = hp_p2
            
            time.sleep(0.05) # 20hz is fine for health monitoring

    def fire(self): pass
