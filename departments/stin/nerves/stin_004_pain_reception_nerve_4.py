import time
import threading
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import get_amsv_block

class STIN_004_PainReceptionNerve4(NerveBase):
    NERVE_ID = "STIN_004"
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
            # Check Bit 2 (S Key)
            if self.amsv_block.keyboard_state & (1 << 2):
                self.amsv_block.ai_target_y = 1.0 # Backward vector
            time.sleep(0.016)
