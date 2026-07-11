import ctypes
import threading
import time
from collections import deque
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class VOID_001_NetworkNerve1(NerveBase):
    """
    CHRONOS TIME-REVERSAL NODE
    Continuously snapshots the 11KB AMSV to RAM. If Spacebar is held, overwrites shared memory to reverse time.
    """
    NERVE_ID = "VOID_001"
    DEPARTMENT = "VOID"
    DIVISION = "network"
    PIPELINE = "performance"
    WIRE_COLOR = "blue"
    
    def __init__(self):
        super().__init__()
        self.chronos_thread = threading.Thread(target=self._chronos_loop, daemon=True)
        self.chronos_thread.start()

    def _chronos_loop(self):
        print("[VOID_001] Chronos Time-Reversal Node ACTIVE.")
        
        # 300 frames = 5 seconds of 60 FPS
        history_buffer = deque(maxlen=300)
        struct_size = ctypes.sizeof(amsv_block)
        struct_addr = ctypes.addressof(amsv_block)
        
        SPACEBAR_BIT = 1 << 4
        
        while True:
            # Check if Spacebar is held down
            if amsv_block.keyboard_state & SPACEBAR_BIT:
                # Time Reversal is ACTIVE!
                if len(history_buffer) > 0:
                    past_state = history_buffer.pop() # Pop the most recent historical state
                    
                    # Forcefully overwrite the entire shared C-Memory block with the past state
                    # This instantly rewinds physics, graphics, and audio for all 480 Nerves!
                    ctypes.memmove(struct_addr, past_state, struct_size)
                    
                    # Ensure the spacebar bit remains pressed in the rewound state so we don't drop out of the loop
                    amsv_block.keyboard_state |= SPACEBAR_BIT
                
            else:
                # Time is flowing normally. Record the current state.
                # bytes(amsv_block) creates an exact byte-for-byte copy of the C-Struct
                current_state = bytes(amsv_block)
                history_buffer.append(current_state)
            
            # Run at 60 FPS
            time.sleep(0.016)

    def fire(self): pass
