import threading
import time
import ctypes
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class ALUS_131_AudioSpatialNerve1(NerveBase):
    """
    PLAYER AUDIO NERVE
    Monitors input and generates retro 8-bit laser sounds when firing.
    """
    NERVE_ID = "ALUS_131"
    DEPARTMENT = "ALUS"
    DIVISION = "audio_spatial"
    PIPELINE = "runtime"
    WIRE_COLOR = "cyan"
    
    def __init__(self):
        super().__init__()
        self.audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        self.audio_thread.start()

    def _play_laser(self):
        import winsound
        winsound.Beep(1200, 30)
        winsound.Beep(800, 30)

    def _audio_loop(self):
        print("[ALUS_131] Player Audio Node ACTIVE (8-bit Mode).")
        user32 = ctypes.windll.user32
        was_firing = False
        
        while True:
            kb = amsv_block.keyboard_state
            ms = amsv_block.mouse_state
            is_firing = (ms & (1 << 0)) != 0 or (kb & (1 << 4)) != 0
            
            if is_firing and not was_firing:
                threading.Thread(target=self._play_laser, daemon=True).start()
                
            was_firing = is_firing
            time.sleep(0.016)

    def fire(self): pass
