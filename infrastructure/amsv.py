import ctypes
from multiprocessing import shared_memory

class EntityState(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("x", ctypes.c_float),
        ("y", ctypes.c_float),
        ("z", ctypes.c_float),
        ("rx", ctypes.c_float),
        ("ry", ctypes.c_float),
        ("rz", ctypes.c_float),
        ("vx", ctypes.c_float),
        ("vy", ctypes.c_float),
        ("vz", ctypes.c_float),
        ("health", ctypes.c_float),
        ("state", ctypes.c_uint32)
    ]

class AtomicMemoryStateVector(ctypes.Structure):
    """
    The Absolute Shared Physical Memory Block.
    No serialization. No Python dicts. Pure C-memory addresses.
    Both Hardware and Python Nerves share this exact silicon space.
    """
    _pack_ = 1  # 1-byte packing ensures zero padding
    _fields_ = [
        # LEGACY: 16 Bytes: Coordinate Matrix (Kept for backward compatibility)
        ("coord_x", ctypes.c_float),
        ("coord_y", ctypes.c_float),
        ("coord_z", ctypes.c_float),
        ("rotation", ctypes.c_float),
        
        # 16 Bytes: Environmental Sensors
        ("cpu_temp", ctypes.c_float),
        ("gpu_load", ctypes.c_float),
        ("ram_usage", ctypes.c_float),
        ("wattage", ctypes.c_float),
        
        # 16 Bytes: Input Bitmask
        ("mouse_state", ctypes.c_uint32),
        ("keyboard_state", ctypes.c_uint32),
        ("controller_1", ctypes.c_uint32),
        ("controller_2", ctypes.c_uint32),
        
        # LEGACY: 16 Bytes: AI Logic / Engine State (Kept for backward compatibility)
        ("ai_target_x", ctypes.c_float),
        ("ai_target_y", ctypes.c_float),
        ("health_state", ctypes.c_float),
        ("time_delta", ctypes.c_float),
        
        # NEW V4 EXPANSION: Array of 256 Entities (11,264 Bytes)
        ("entity_count", ctypes.c_uint32),
        ("entities", EntityState * 256)
    ]

# Global reference to prevent GC from closing the shared memory block
_shm = None

def get_amsv_block():
    global _shm
    mem_name = "SOLO_ROCK_AMSV"
    size = ctypes.sizeof(AtomicMemoryStateVector)
    
    try:
        # Try to connect to an existing block created by the OS Launcher
        _shm = shared_memory.SharedMemory(name=mem_name)
    except FileNotFoundError:
        # If it doesn't exist, we are the OS Launcher, create it
        _shm = shared_memory.SharedMemory(name=mem_name, create=True, size=size)
        # Initialize memory with zeros
        _shm.buf[:size] = bytearray(size)
        
    # Cast the raw memory buffer directly to our C-Struct pointer!
    amsv_block = AtomicMemoryStateVector.from_buffer(_shm.buf)
    return amsv_block

def cleanup_amsv():
    global _shm
    if _shm:
        _shm.close()
        try:
            _shm.unlink()
        except FileNotFoundError:
            pass

# Every time a process imports this file, it will attach to the SAME OS memory block.
amsv_block = get_amsv_block()
