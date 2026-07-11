import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import get_amsv_block

class STIN_009_PainReceptionNerve9(NerveBase):
    NERVE_ID = "STIN_009"
    DEPARTMENT = "STIN"
    DIVISION = "pain_reception"
    PIPELINE = "input"
    WIRE_COLOR = "teal"
    
    def __init__(self):
        super().__init__()
        self.amsv_block = get_amsv_block()
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        
    def _monitor_loop(self):
        while True:
            # Check Bit 5 (Shift Key)
            if self.amsv_block.keyboard_state & (1 << 5):
                # Set a stamina/sprint modifier flag
                self.amsv_block.health_state = 2.0 # Arbitrary modifier for 'sprinting'
            else:
                self.amsv_block.health_state = 1.0 # Normal walking
            time.sleep(0.016)
