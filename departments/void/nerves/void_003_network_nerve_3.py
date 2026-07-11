import threading
import time
import socket
import ctypes
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class VOID_003_NetworkNerve3(NerveBase):
    """
    CLIENT NERVE (UDP CLIENT)
    Receives the 11KB AMSV memory block from the Host and forcefully overwrites local memory.
    Transmits Player 2's keyboard inputs to the Host.
    """
    NERVE_ID = "VOID_003"
    DEPARTMENT = "VOID"
    DIVISION = "network"
    PIPELINE = "runtime"
    WIRE_COLOR = "cyan"
    
    def __init__(self):
        super().__init__()
        import sys
        if "--client" not in sys.argv:
            print("[VOID_003] Running in Host mode. Client Nerve disabled.")
            return
            
        self.host = "127.0.0.1"
        self.port_in = 9999
        self.port_out = 9998
        
        self.sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_in.bind(("0.0.0.0", self.port_in))
        self.sock_in.setblocking(False)
        
        self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.transmit_thread = threading.Thread(target=self._transmit_loop, daemon=True)
        
        self.receive_thread.start()
        self.transmit_thread.start()

    def _receive_loop(self):
        print(f"[VOID_003] Client Listening for AMSV payload on port {self.port_in}...")
        expected_size = ctypes.sizeof(amsv_block)
        while True:
            try:
                data, addr = self.sock_in.recvfrom(65507)
                if data and len(data) == expected_size:
                    # THE ZERO-BRIDGE MEMORY INJECTION
                    # Forcefully overwrite the entire 11KB C-Struct with the network payload
                    ctypes.memmove(ctypes.addressof(amsv_block), data, expected_size)
            except BlockingIOError:
                pass
            except Exception as e:
                pass
            time.sleep(0.001) # Poll aggressively for minimal latency

    def _transmit_loop(self):
        print(f"[VOID_003] Client Transmitting Player 2 inputs to port {self.port_out}...")
        while True:
            try:
                # Transmit our local keyboard state (from STIN) to the Host
                # The Host will write this to amsv_block.controller_1
                p2_input = amsv_block.keyboard_state
                self.sock_out.sendto(p2_input.to_bytes(4, byteorder='little'), (self.host, self.port_out))
            except Exception as e:
                pass
            time.sleep(0.016) # 60 FPS Sync

    def fire(self): pass
