import ctypes
import time
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class STIN_002_MouseNerve2(NerveBase):
    NERVE_ID = "STIN_002"
    DEPARTMENT = "STIN"
    DIVISION = "sensory_transmission"
    PIPELINE = "runtime"
    WIRE_COLOR = "red"

    def __init__(self):
        super().__init__()
        self.user32 = ctypes.windll.user32

    def fire(self):
        while True:
            state = 0
            if (self.user32.GetAsyncKeyState(0x01) & 0x8000) != 0: state |= (1 << 0) # Left Click
            
            amsv_block.mouse_state = state
            time.sleep(0.016)
