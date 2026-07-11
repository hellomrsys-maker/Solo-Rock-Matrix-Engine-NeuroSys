import ctypes
import math
import threading
import time
import sys
import os
from multiprocessing import shared_memory

# -------------------------------------------------------------------------
# 1. ZERO-BRIDGE SYNCHRONOUS MEMORY ARCHITECTURE (AMSV)
# -------------------------------------------------------------------------
class EntityState(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("x", ctypes.c_float), ("y", ctypes.c_float), ("z", ctypes.c_float),
        ("rx", ctypes.c_float), ("ry", ctypes.c_float), ("rz", ctypes.c_float),
        ("vx", ctypes.c_float), ("vy", ctypes.c_float), ("vz", ctypes.c_float),
        ("health", ctypes.c_float), ("state", ctypes.c_uint32)
    ]

class AtomicMemoryStateVector(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("coord_x", ctypes.c_float), ("coord_y", ctypes.c_float), ("coord_z", ctypes.c_float), ("rotation", ctypes.c_float),
        ("cpu_temp", ctypes.c_float), ("gpu_load", ctypes.c_float), ("ram_usage", ctypes.c_float), ("wattage", ctypes.c_float),
        ("mouse_state", ctypes.c_uint32), ("keyboard_state", ctypes.c_uint32), ("controller_1", ctypes.c_uint32), ("controller_2", ctypes.c_uint32),
        ("ai_target_x", ctypes.c_float), ("ai_target_y", ctypes.c_float), ("health_state", ctypes.c_float), ("time_delta", ctypes.c_float),
        ("entity_count", ctypes.c_uint32), ("entities", EntityState * 256)
    ]

_shm = None
def get_amsv_block():
    global _shm
    mem_name = "SOLO_ROCK_MASTER"
    size = ctypes.sizeof(AtomicMemoryStateVector)
    try:
        _shm = shared_memory.SharedMemory(name=mem_name)
    except FileNotFoundError:
        _shm = shared_memory.SharedMemory(name=mem_name, create=True, size=size)
        _shm.buf[:size] = bytearray(size)
    return AtomicMemoryStateVector.from_buffer(_shm.buf)

amsv_block = get_amsv_block()

# -------------------------------------------------------------------------
# 2. WORLD DATA
# -------------------------------------------------------------------------
WORLD_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,1,1,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# -------------------------------------------------------------------------
# 3. AI HARDWARE CONTROLLER (THE OVERLORD)
# -------------------------------------------------------------------------
def get_cpu_times():
    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", ctypes.c_uint), ("dwHighDateTime", ctypes.c_uint)]
    idle, kernel, user = FILETIME(), FILETIME(), FILETIME()
    ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user))
    def ft_to_int(ft): return (ft.dwHighDateTime << 32) | ft.dwLowDateTime
    return ft_to_int(idle), ft_to_int(kernel), ft_to_int(user)

def ai_hardware_overlord():
    print("[AI OVERLORD] Native Hardware Monitor Online. Reading CPU Load...")
    last_idle, last_kernel, last_user = get_cpu_times()
    
    while True:
        time.sleep(1.0) # Check every second
        idle, kernel, user = get_cpu_times()
        
        sys_diff = (kernel + user) - (last_kernel + last_user)
        idle_diff = idle - last_idle
        
        if sys_diff > 0:
            cpu_usage = ((sys_diff - idle_diff) / sys_diff) * 100.0
        else:
            cpu_usage = 0.0
            
        # Write hardware state natively into the Matrix (Zero-Bridge)
        amsv_block.cpu_temp = cpu_usage 
        
        # DYNAMIC THROTTLING LOGIC
        # If CPU > 50%, AI forcefully limits Software Engine capacity to prevent overheating.
        if cpu_usage > 50.0:
            amsv_block.gpu_load = max(0.2, amsv_block.gpu_load - 0.2)
            print(f"[*] WARNING! CPU OVERHEATING ({cpu_usage:.1f}%). AI Throttling Software to {amsv_block.gpu_load*100:.0f}% capacity!")
        else:
            amsv_block.gpu_load = min(1.0, amsv_block.gpu_load + 0.1)
            print(f"[*] AI Optimal Control. CPU at {cpu_usage:.1f}%. Software Engine allowed {amsv_block.gpu_load*100:.0f}% capacity.")
            
        last_idle, last_kernel, last_user = idle, kernel, user

# -------------------------------------------------------------------------
# 4. SENSORY INPUT (STIN)
# -------------------------------------------------------------------------
def input_nerve():
    user32 = ctypes.windll.user32
    while True:
        state = 0
        if (user32.GetAsyncKeyState(0x57) & 0x8000) != 0: state |= (1 << 0) # W
        if (user32.GetAsyncKeyState(0x41) & 0x8000) != 0: state |= (1 << 1) # A
        if (user32.GetAsyncKeyState(0x53) & 0x8000) != 0: state |= (1 << 2) # S
        if (user32.GetAsyncKeyState(0x44) & 0x8000) != 0: state |= (1 << 3) # D
        if (user32.GetAsyncKeyState(0x0D) & 0x8000) != 0: state |= (1 << 7) # Enter
        amsv_block.keyboard_state = state
        time.sleep(0.016)

# -------------------------------------------------------------------------
# 5. SOFTWARE ENGINE: RENDERER (PPVO)
# -------------------------------------------------------------------------
def render_nerve():
    user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    hbrush_floor, hbrush_ceil = gdi32.CreateSolidBrush(0x00333333), gdi32.CreateSolidBrush(0x00111111)
    hbrush_wall = gdi32.CreateSolidBrush(0x0000FF00) # Green Walls!
    
    screen_w, screen_h = 800, 600
    print("[SOFTWARE ENGINE] 3D Raycaster Matrix Online.")
    
    while True:
        try:
            hdc = user32.GetDC(0)
            if hdc:
                # ---------------- BOOT MENU ----------------
                if amsv_block.state == 5:
                    rc_full = RECT(0, 0, screen_w, screen_h)
                    user32.FillRect(hdc, ctypes.byref(rc_full), gdi32.CreateSolidBrush(0x000000))
                    gdi32.SetTextColor(hdc, 0x00FF00)
                    gdi32.SetBkColor(hdc, 0x000000)
                    gdi32.SetBkMode(hdc, 2)
                    title = "=====================================================\n"
                    title += "        SOLO ROCK V4: MONOLITHIC AI EDITION\n"
                    title += "=====================================================\n\n"
                    title += "LORE:\n"
                    title += "The AI Overlord controls hardware capacity in real-time.\n"
                    title += "It bridges the gap between Software and Hardware.\n\n"
                    title += "CONTROLS: WASD to Move.\n\n"
                    title += "PRESS ENTER TO INITIALIZE NEURAL LINK...\n"
                    user32.DrawTextW(hdc, title, -1, ctypes.byref(rc_full), 0x0000)
                    user32.ReleaseDC(0, hdc)
                    time.sleep(0.016)
                    continue

                # ---------------- THE MATRIX ----------------
                me = amsv_block.entities[0]
                px, py, pa = me.x / 100.0 + 8.0, me.y / 100.0 + 8.0, me.ry
                
                # Clear Screen
                user32.FillRect(hdc, ctypes.byref(RECT(0, 0, screen_w, screen_h // 2)), hbrush_ceil)
                user32.FillRect(hdc, ctypes.byref(RECT(0, screen_h // 2, screen_w, screen_h)), hbrush_floor)
                
                # *** AI HARDWARE THROTTLING IN ACTION ***
                # The AI modifies amsv_block.gpu_load based on CPU temp!
                # If Overheating, Raycaster resolution drops from 160 rays down to 32!
                throttle = max(0.2, min(1.0, amsv_block.gpu_load))
                num_rays = int(160 * throttle) 
                strip_width = screen_w // num_rays
                
                fov = math.pi / 3.0
                for r in range(num_rays):
                    ray_angle = (pa - fov / 2.0) + (float(r) / float(num_rays)) * fov
                    eye_x, eye_y = math.cos(ray_angle), math.sin(ray_angle)
                    
                    dist, hit = 0.0, False
                    while not hit and dist < 20.0:
                        dist += 0.2
                        tx, ty = int(px + eye_x * dist), int(py + eye_y * dist)
                        if tx < 0 or tx >= 16 or ty < 0 or ty >= 16:
                            hit = True; dist = 20.0
                        elif WORLD_MAP[ty][tx] == 1:
                            hit = True
                    
                    ceiling = float(screen_h / 2.0) - screen_h / float(dist)
                    floor = screen_h - ceiling
                    
                    rc_wall = RECT(r * strip_width, int(ceiling), (r + 1) * strip_width, int(floor))
                    user32.FillRect(hdc, ctypes.byref(rc_wall), hbrush_wall)
                
                # Draw Minimap Radar (AI CPU Usage indicator text)
                rc_cpu = RECT(10, 10, 400, 50)
                gdi32.SetTextColor(hdc, 0x000000FF if amsv_block.cpu_temp > 50 else 0x00FFFFFF)
                gdi32.SetBkMode(hdc, 1)
                user32.DrawTextW(hdc, f"CPU LOAD: {amsv_block.cpu_temp:.1f}% | ENGINE CAPACITY: {amsv_block.gpu_load*100:.0f}%", -1, ctypes.byref(rc_cpu), 0)

                user32.ReleaseDC(0, hdc)
                
                # *** AI FPS CAP THROTTLING ***
                # If Overheating, the frame rate is forcibly capped!
                time.sleep(0.016 / throttle) 
                
        except Exception:
            pass

# -------------------------------------------------------------------------
# 6. SOFTWARE ENGINE: PHYSICS (CAIN)
# -------------------------------------------------------------------------
def physics_nerve():
    amsv_block.entities[0].x, amsv_block.entities[0].y = -650.0, -650.0 # Spawn at 1,1
    while True:
        me, kb = amsv_block.entities[0], amsv_block.keyboard_state
        if amsv_block.state == 5:
            if (kb & (1 << 7)) != 0: amsv_block.state = 0 # Enter
            time.sleep(0.016)
            continue
            
        speed = 10.0
        new_x, new_y = me.x, me.y
        if (kb & (1 << 0)) != 0: # W
            new_x += math.cos(me.ry) * speed; new_y += math.sin(me.ry) * speed
        if (kb & (1 << 2)) != 0: # S
            new_x -= math.cos(me.ry) * speed; new_y -= math.sin(me.ry) * speed
        if (kb & (1 << 1)) != 0: me.ry -= 0.1 # A
        if (kb & (1 << 3)) != 0: me.ry += 0.1 # D
        
        # Collision
        grid_x, grid_y = int(new_x / 100.0 + 8.0), int(new_y / 100.0 + 8.0)
        if 0 <= grid_x < 16 and 0 <= grid_y < 16:
            if WORLD_MAP[grid_y][grid_x] == 0:
                me.x, me.y = new_x, new_y
                
        time.sleep(0.016)

# -------------------------------------------------------------------------
# 7. GRAND UNIFICATION ENTRY POINT
# -------------------------------------------------------------------------
if __name__ == '__main__':
    print("\n=========================================================")
    print(" SOLO ROCK V4: MONOLITHIC AI EDITION")
    print(" Bridging Software Engine with AI Hardware Controller")
    print("=========================================================\n")
    
    amsv_block.state = 5
    amsv_block.gpu_load = 1.0 
    
    threads = [
        threading.Thread(target=ai_hardware_overlord, daemon=True),
        threading.Thread(target=input_nerve, daemon=True),
        threading.Thread(target=physics_nerve, daemon=True)
    ]
    for t in threads: t.start()
    
    try:
        render_nerve() # Blocks main thread to keep GDI happy
    except KeyboardInterrupt:
        print("\n[SYSTEM] Terminating Neural Link...")
