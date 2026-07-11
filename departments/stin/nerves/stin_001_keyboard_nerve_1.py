import ctypes
import time
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class STIN_001_KeyboardNerve1(NerveBase):
    NERVE_ID = "STIN_001"
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
            if (self.user32.GetAsyncKeyState(0x57) & 0x8000) != 0: state |= (1 << 0) # W
            if (self.user32.GetAsyncKeyState(0x41) & 0x8000) != 0: state |= (1 << 1) # A
            if (self.user32.GetAsyncKeyState(0x53) & 0x8000) != 0: state |= (1 << 2) # S
            if (self.user32.GetAsyncKeyState(0x44) & 0x8000) != 0: state |= (1 << 3) # D
            if (self.user32.GetAsyncKeyState(0x20) & 0x8000) != 0: state |= (1 << 4) # Space
            if (self.user32.GetAsyncKeyState(0x10) & 0x8000) != 0: state |= (1 << 5) # Shift
            if (self.user32.GetAsyncKeyState(0x45) & 0x8000) != 0: state |= (1 << 6) # E
            if (self.user32.GetAsyncKeyState(0x0D) & 0x8000) != 0: state |= (1 << 7) # Enter
            
            amsv_block.keyboard_state = state
            time.sleep(0.016)
