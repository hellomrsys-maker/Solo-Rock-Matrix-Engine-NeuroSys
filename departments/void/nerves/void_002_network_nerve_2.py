import threading
import time
import socket
import ctypes
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

class VOID_002_NetworkNerve2(NerveBase):
    """
    HOST NERVE (UDP SERVER)
    Broadcasts the 11KB AMSV memory block to the Client.
    Listens for Client inputs and writes them to controller_1.
    """
    NERVE_ID = "VOID_002"
    DEPARTMENT = "VOID"
    DIVISION = "network"
    PIPELINE = "runtime"
    WIRE_COLOR = "cyan"
    
    def __init__(self):
        super().__init__()
        import sys
        if "--client" in sys.argv:
            print("[VOID_002] Running in Client mode. Host Nerve disabled.")
            return
            
        self.host = "127.0.0.1"
        self.port_out = 9999
        self.port_in = 9998
        
        self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_in.bind(("0.0.0.0", self.port_in))
        self.sock_in.setblocking(False)
        
        self.client_address = None
        
        self.broadcast_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        
        self.broadcast_thread.start()
        self.receive_thread.start()

    def _broadcast_loop(self):
        print(f"[VOID_002] Host Broadcasting AMSV on port {self.port_out}...")
        while True:
            try:
                # Dump the exact 11KB C-struct memory bytes
                amsv_bytes = bytes(amsv_block)
                # Max UDP size is 65507, 11KB is well within limits.
                if self.client_address:
                    self.sock_out.sendto(amsv_bytes, self.client_address)
                else:
                    # Broadcast blindly until we hear from a client
                    self.sock_out.sendto(amsv_bytes, (self.host, self.port_out))
            except Exception as e:
                pass
            time.sleep(0.016) # 60 FPS Sync

    def _receive_loop(self):
        print(f"[VOID_002] Host Listening for Player 2 Inputs on port {self.port_in}...")
        while True:
            try:
                data, addr = self.sock_in.recvfrom(1024)
                if data:
                    self.client_address = addr # Remember client address for broadcasting
                    # Parse 4-byte uint32 for Player 2 keyboard state
                    p2_input = int.from_bytes(data, byteorder='little')
                    amsv_block.controller_1 = p2_input
            except BlockingIOError:
                pass
            except Exception as e:
                pass
            time.sleep(0.016)

    def fire(self): pass
