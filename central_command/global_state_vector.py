class GlobalStateVector:
    def __init__(self):
        self.amsv_memory = bytearray(64) # The 64-byte Atomic Memory State Vector
