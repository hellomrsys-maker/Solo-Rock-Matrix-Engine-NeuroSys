import ctypes
import math
import threading
import time
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# GDI Constants
PS_SOLID = 0
SRCCOPY = 0x00CC0020
LR_LOADFROMFILE = 0x00000010
IMAGE_BITMAP = 0

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

# GDI functions
StretchBlt = gdi32.StretchBlt
CreateCompatibleDC = gdi32.CreateCompatibleDC
SelectObject = gdi32.SelectObject
DeleteDC = gdi32.DeleteDC
DeleteObject = gdi32.DeleteObject
LoadImageW = user32.LoadImageW
DrawTextW = user32.DrawTextW
SetTextColor = gdi32.SetTextColor
SetBkMode = gdi32.SetBkMode

try:
    msimg32 = ctypes.windll.msimg32
    TransparentBlt = msimg32.TransparentBlt
except:
    pass

class PPVO_241_UIOverlayNerve1(NerveBase):
    """
    TRUE CPU RAYCASTER (DOOM-STYLE)
    Casts rays across a 2D map to render 3D walls directly to the GDI desktop.
    """
    NERVE_ID = "PPVO_241"
    DEPARTMENT = "PPVO"
    DIVISION = "ui_overlay"
    PIPELINE = "render"
    WIRE_COLOR = "red"
    
    def __init__(self):
        super().__init__()
        import sys
        
        self.is_client = "--client" in sys.argv
        from infrastructure.world_map import WORLD_MAP
        self.world_map = WORLD_MAP
        
        self.render_thread = threading.Thread(target=self._render_loop, daemon=True)
        self.render_thread.start()

    def _render_loop(self):
        print("[PPVO_241] TRUE CPU RAYCASTER ACTIVE.")
        
        screen_w = 800
        screen_h = 600
        
        # We will draw 160 vertical strips to save CPU (800 / 5)
        num_rays = 160
        strip_width = screen_w // num_rays
        
        fov = math.pi / 3.0 # 60 degrees
        
        # Brushes
        hbrush_floor = gdi32.CreateSolidBrush(0x00333333) # Dark Gray
        hbrush_ceil = gdi32.CreateSolidBrush(0x00111111)  # Very Dark Gray
        hbrush_wall1 = gdi32.CreateSolidBrush(0x00888888) # Light Gray
        hbrush_wall2 = gdi32.CreateSolidBrush(0x00555555) # Med Gray
        hbrush_red = gdi32.CreateSolidBrush(0x000000FF)   # Red (Swarm)
        hbrush_blue = gdi32.CreateSolidBrush(0x00FF0000)  # Blue (P2)
        hbrush_green = gdi32.CreateSolidBrush(0x0000FF00) # Green (P1)
        hbrush_yellow = gdi32.CreateSolidBrush(0x0000FFFF)# Yellow (Bullets)
        hbrush_white = gdi32.CreateSolidBrush(0x00FFFFFF) # White (Microglia/Antibodies)
        hbrush_cyan = gdi32.CreateSolidBrush(0x00FFFF00)  # Cyan (T-Cells)
        hbrush_pink = gdi32.CreateSolidBrush(0x00FF00FF)  # Pink (Stem Cells)
        hbrush_yellow = gdi32.CreateSolidBrush(0x0000FFFF) # Yellow (Glitched)
        
        # Load Texture
        texWidth, texHeight = 1024, 1024
        
        # PyInstaller extracts bundled files to sys._MEIPASS
        import sys
        import os
        if hasattr(sys, '_MEIPASS'):
            tex_path = os.path.join(sys._MEIPASS, "wall_texture.bmp")
            gun_idle_path = os.path.join(sys._MEIPASS, "gun_idle.bmp")
            gun_fire_path = os.path.join(sys._MEIPASS, "gun_fire.bmp")
        else:
            tex_path = "wall_texture.bmp"
            gun_idle_path = "gun_idle.bmp"
            gun_fire_path = "gun_fire.bmp"
            
        hBmp = LoadImageW(None, tex_path, IMAGE_BITMAP, texWidth, texHeight, LR_LOADFROMFILE)
        
        hGunIdle = LoadImageW(None, gun_idle_path, IMAGE_BITMAP, 512, 512, LR_LOADFROMFILE)
        hGunFire = LoadImageW(None, gun_fire_path, IMAGE_BITMAP, 512, 512, LR_LOADFROMFILE)
        
        SetBkColor = gdi32.SetBkColor
        
        while True:
            try:
                hdc = user32.GetDC(0)
                if hdc:
                    # Phase 19: Boot Menu State
                    if amsv_block.state == 5:
                        rc_full = RECT(0, 0, screen_w, screen_h)
                        user32.FillRect(hdc, ctypes.byref(rc_full), gdi32.CreateSolidBrush(0x000000))
                        
                        SetTextColor(hdc, 0x00FF00) # Green text
                        SetBkColor(hdc, 0x000000)   # Black background
                        SetBkMode(hdc, 2)           # OPAQUE
                        
                        title = "=====================================================\n"
                        title += "          SOLO ROCK V4: MATRIX ENGINE\n"
                        title += "=====================================================\n\n"
                        title += "                  [ SYSTEM BOOTING ]\n\n"
                        title += "LORE:\n"
                        title += "You are a sentient algorithm trapped in a biological simulation.\n"
                        title += "Find the Green Source Code Key. Escape the Matrix.\n\n"
                        title += "CONTROLS:\n"
                        title += "W, A, S, D     : Move\n"
                        title += "LEFT, RIGHT    : Rotate Camera\n"
                        title += "SPACEBAR       : Fire Weapon\n"
                        title += "SHIFT          : Trigger EMP Hack\n"
                        title += "E              : System Overclock\n\n"
                        title += "PRESS ENTER TO INITIALIZE NEURAL LINK...\n"
                        
                        DrawTextW(hdc, title, -1, ctypes.byref(rc_full), 0x0000)
                        user32.ReleaseDC(0, hdc)
                        time.sleep(0.016)
                        continue
                        
                    # Choose which entity is the local camera
                    my_id = 200 if self.is_client else 0
                    px = amsv_block.entities[my_id].x / 100.0 + 8.0 # Scale and offset to map
                    py = amsv_block.entities[my_id].y / 100.0 + 8.0
                    pa = amsv_block.entities[my_id].ry # Look Angle
                    
                    # Phase 15: Overclock FOV Warp
                    if amsv_block.entities[181].z > 0.0:
                        fov = math.pi / 2.0 # 90 degrees (Warp speed!)
                    else:
                        fov = math.pi / 3.0 # 60 degrees (Normal)
                    # 1. Clear Screen (Ceil and Floor)
                    rc_ceil = RECT(0, 0, screen_w, screen_h // 2)
                    rc_floor = RECT(0, screen_h // 2, screen_w, screen_h)
                    user32.FillRect(hdc, ctypes.byref(rc_ceil), hbrush_ceil)
                    user32.FillRect(hdc, ctypes.byref(rc_floor), hbrush_floor)
                    
                    z_buffer = [0] * num_rays
                    
                    # 2. Cast Rays
                    for r in range(num_rays):
                        # Ray angle
                        ray_angle = (pa - fov / 2.0) + (float(r) / float(num_rays)) * fov
                        
                        eye_x = math.cos(ray_angle)
                        eye_y = math.sin(ray_angle)
                        
                        distance_to_wall = 0.0
                        hit_wall = False
                        hit_boundary = False
                        
                        while not hit_wall and distance_to_wall < 20.0:
                            distance_to_wall += 0.1
                            test_x = int(px + eye_x * distance_to_wall)
                            test_y = int(py + eye_y * distance_to_wall)
                            
                            if test_x < 0 or test_x >= 16 or test_y < 0 or test_y >= 16:
                                hit_wall = True
                                distance_to_wall = 20.0
                            else:
                                if self.world_map[test_y][test_x] == 1:
                                    hit_wall = True
                                    
                        z_buffer[r] = distance_to_wall
                        
                        # Calculate exact hit point for texture mapping
                        hit_x_exact = px + eye_x * distance_to_wall
                        hit_y_exact = py + eye_y * distance_to_wall
                        
                        # Determine if we hit a vertical (x) or horizontal (y) wall
                        diff_x = hit_x_exact - math.floor(hit_x_exact)
                        diff_y = hit_y_exact - math.floor(hit_y_exact)
                        
                        # The side with a fractional part closer to 0 or 1 is the face we hit
                        if abs(diff_x - 0.5) > abs(diff_y - 0.5):
                            tex_x = int(diff_x * texWidth)
                        else:
                            tex_x = int(diff_y * texWidth)
                            
                        # Keep tex_x in bounds
                        tex_x = max(0, min(tex_x, texWidth - 1))
                        
                        # Calculate wall height based on distance
                        ceiling = float(screen_h / 2.0) - screen_h / float(distance_to_wall)
                        floor = screen_h - ceiling
                        
                        wall_height = int(floor - ceiling)
                        if wall_height < 0: wall_height = 0
                        
                        rc_wall = RECT(r * strip_width, int(ceiling), (r + 1) * strip_width, int(floor))
                        
                        # Texture Mapping via StretchBlt
                        if amsv_block.state == 4:
                            # Phase 16: Matrix Collapse!
                            user32.FillRect(hdc, ctypes.byref(rc_wall), hbrush_green)
                        elif hBmp:
                            hMemDC = CreateCompatibleDC(hdc)
                            SelectObject(hMemDC, hBmp)
                            StretchBlt(hdc, r * strip_width, int(ceiling), strip_width, wall_height, hMemDC, tex_x, 0, 1, texHeight, SRCCOPY)
                            DeleteDC(hMemDC)
                        else:
                            # Fallback shading
                            brush = hbrush_wall1 if distance_to_wall < 10 else hbrush_wall2
                            user32.FillRect(hdc, ctypes.byref(rc_wall), brush)
                        
                    # 3. Render Sprites (Entities)
                    sprites = []
                    
                    # Add Macrophage Final Boss
                    for i in range(176, 180):
                        if amsv_block.entities[i].health > 0:
                            brush = hbrush_white
                            if amsv_block.entities[i].vx == -1.0: brush = hbrush_yellow
                            sprites.append((amsv_block.entities[i], brush, 3.0 if i == 176 else 1.5))
                            
                    # Add Source Code Key (Phase 16)
                    if amsv_block.entities[182].z > 0:
                        sprites.append((amsv_block.entities[182], hbrush_green, 1.5))                       
                    # Add Blood Vessels
                    for i in range(91, 96):
                        if amsv_block.entities[i].health > 0:
                            sprites.append((amsv_block.entities[i], hbrush_blue, 1.5))
                            
                    # Add Swarm
                    for i in range(61, 91):
                        if amsv_block.entities[i].z > 0:
                            brush = hbrush_green if amsv_block.entities[i].vx == 1.0 else hbrush_red
                            sprites.append((amsv_block.entities[i], brush, 1.0))
                            
                    # Add Microglia
                    for i in range(96, 99):
                        if amsv_block.entities[i].health > 0:
                            sprites.append((amsv_block.entities[i], hbrush_white, 1.2))
                            
                    # Add Bullets
                    for i in range(1, 11):
                        if amsv_block.entities[i].z > 0:
                            sprites.append((amsv_block.entities[i], hbrush_yellow, 0.2))
                            
                    # Add Enemy Lasers
                    for i in range(100, 131):
                        if amsv_block.entities[i].z > 0:
                            sprites.append((amsv_block.entities[i], hbrush_red, 0.3))
                            
                    # Add T-Cells
                    for i in range(131, 136):
                        if amsv_block.entities[i].z > 0:
                            sprites.append((amsv_block.entities[i], hbrush_cyan, 1.2))
                            
                    # Add Antibodies
                    for i in range(136, 151):
                        if amsv_block.entities[i].z > 0:
                            sprites.append((amsv_block.entities[i], hbrush_white, 0.2))
                            
                    # Add Stem Cells
                    for i in range(151, 156):
                        if amsv_block.entities[i].z > 0:
                            sprites.append((amsv_block.entities[i], hbrush_pink, 1.0))
                            
                    # Add ATP Payloads
                    for i in range(156, 166):
                        if amsv_block.entities[i].z > 0:
                            sprites.append((amsv_block.entities[i], hbrush_yellow, 0.5))
                            
                    # Add Astrocytes (BBB Shield)
                    for i in range(166, 176):
                        if amsv_block.entities[i].z > 0:
                            sprites.append((amsv_block.entities[i], hbrush_cyan, 0.8))
                            
                    # Add Macrophage Final Boss
                    for i in range(176, 180):
                        if amsv_block.entities[i].health > 0:
                            sprites.append((amsv_block.entities[i], hbrush_white, 2.5)) # Giant size!
                            
                    # Add Other Player
                    other_id = 0 if self.is_client else 200
                    if amsv_block.entities[other_id].health > 0:
                        brush = hbrush_green if self.is_client else hbrush_blue
                        sprites.append((amsv_block.entities[other_id], brush, 1.0))
                        
                    # Sort sprites by distance from player (Painter's Algorithm for sprites)
                    def get_dist(s):
                        sx = s[0].x / 100.0 + 8.0
                        sy = s[0].y / 100.0 + 8.0
                        return math.sqrt((px - sx)**2 + (py - sy)**2)
                        
                    sprites.sort(key=get_dist, reverse=True)
                    
                    for sprite, brush, scale in sprites:
                        sx = sprite.x / 100.0 + 8.0
                        sy = sprite.y / 100.0 + 8.0
                        
                        dx = sx - px
                        dy = sy - py
                        
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist < 0.1: continue
                        
                        sprite_angle = math.atan2(dy, dx) - pa
                        
                        # Normalize angle
                        while sprite_angle < -math.pi: sprite_angle += 2.0 * math.pi
                        while sprite_angle > math.pi: sprite_angle -= 2.0 * math.pi
                        
                        # Is it in FOV?
                        if abs(sprite_angle) < (fov / 2.0) + 0.2:
                            # Map angle to screen X
                            screen_x = (0.5 * (sprite_angle / (fov / 2.0)) + 0.5) * screen_w
                            
                            sprite_height = int((screen_h / dist) * scale)
                            sprite_width = sprite_height
                            
                            sprite_ceiling = int((screen_h / 2.0) - (sprite_height / 2.0))
                            
                            # Simple occlusion: check against z_buffer center ray
                            ray_index = int((screen_x / screen_w) * num_rays)
                            if 0 <= ray_index < num_rays:
                                if z_buffer[ray_index] > dist:
                                    rc_sprite = RECT(
                                        int(screen_x - sprite_width/2),
                                        sprite_ceiling,
                                        int(screen_x + sprite_width/2),
                                        sprite_ceiling + sprite_height
                                    )
                            if sprite.vx == -1.0: # Glitched / Paralyzed!
                                user32.FillRect(hdc, ctypes.byref(rc_sprite), hbrush_yellow)
                            else:
                                user32.FillRect(hdc, ctypes.byref(rc_sprite), brush)

                    # 4. Phase 14: Cybernetic EMP Blast Overlay
                    emp = amsv_block.entities[180]
                    if emp.z > 0.0:
                        emp_r = int((emp.health / 600.0) * screen_h * 1.5) # Expand massively
                        cx = int(screen_w / 2)
                        cy = int(screen_h / 2)
                        
                        hpen_cyan = gdi32.CreatePen(0, 15, 0x00FFFF00) # Thick cyan line
                        old_pen = gdi32.SelectObject(hdc, hpen_cyan)
                        old_brush = gdi32.SelectObject(hdc, gdi32.GetStockObject(5)) # NULL_BRUSH
                        
                        gdi32.Ellipse(hdc, cx - emp_r, cy - emp_r, cx + emp_r, cy + emp_r)
                        
                        gdi32.SelectObject(hdc, old_pen)
                        gdi32.SelectObject(hdc, old_brush)
                        gdi32.DeleteObject(hpen_cyan)

                    # 5. Draw Weapon View-Model (Bottom Center)
                    kb = amsv_block.keyboard_state
                    ms = amsv_block.mouse_state
                    is_firing = (ms & (1 << 0)) != 0 or (kb & (1 << 4)) != 0
                    hGun = hGunFire if is_firing else hGunIdle
                    
                    if hGun:
                        hMemDC_Gun = CreateCompatibleDC(hdc)
                        SelectObject(hMemDC_Gun, hGun)
                        gun_w, gun_h = 400, 400
                        gun_x = (screen_w // 2) - (gun_w // 2)
                        gun_y = screen_h - gun_h
                        
                        # Magenta (0xFF00FF) is 0x00FF00FF in COLORREF (0x00bbggrr)
                        TransparentBlt(hdc, gun_x, gun_y, gun_w, gun_h, hMemDC_Gun, 0, 0, 512, 512, 0x00FF00FF)
                        DeleteDC(hMemDC_Gun)
                    
                    # 5. HUD (Health Bar)
                    hp = amsv_block.entities[my_id].health
                    state = amsv_block.state
                    
                    if hp <= 0 or state == 1:
                        rc_dead = RECT(0, 0, screen_w, screen_h)
                        user32.FillRect(hdc, ctypes.byref(rc_dead), hbrush_red)
                        SetTextColor(hdc, 0x00FFFFFF)
                        SetBkMode(hdc, 1)
                        rc_text = RECT(screen_w//2 - 150, screen_h//2, screen_w//2 + 150, screen_h//2 + 50)
                        DrawTextW(hdc, ctypes.c_wchar_p("GAME OVER - SYNAPTIC FAILURE"), -1, ctypes.byref(rc_text), 0)
                    elif state == 2:
                        rc_win = RECT(0, 0, screen_w, screen_h)
                        user32.FillRect(hdc, ctypes.byref(rc_win), hbrush_green)
                        SetTextColor(hdc, 0x00FFFFFF)
                        SetBkMode(hdc, 1)
                        rc_text = RECT(screen_w//2 - 150, screen_h//2, screen_w//2 + 150, screen_h//2 + 50)
                        DrawTextW(hdc, ctypes.c_wchar_p("NEURAL ESCAPE SUCCESSFUL"), -1, ctypes.byref(rc_text), 0)
                    else:
                        rc_bg = RECT(50, 50, 350, 80)
                        user32.FillRect(hdc, ctypes.byref(rc_bg), hbrush_red)
                        hp_width = int((hp / 100.0) * 300)
                        rc_fg = RECT(50, 50, 50 + hp_width, 80)
                        user32.FillRect(hdc, ctypes.byref(rc_fg), hbrush_green)
                        
                        if state == 3:
                            rc_key = RECT(50, 100, 100, 130)
                            user32.FillRect(hdc, ctypes.byref(rc_key), hbrush_yellow)
                            SetTextColor(hdc, 0x00000000)
                            SetBkMode(hdc, 1)
                            DrawTextW(hdc, ctypes.c_wchar_p("KEY"), -1, ctypes.byref(rc_key), 0)
                            
                        # Phase 20: Real-Time Radar Minimap
                        map_size = 16
                        cell_size = 8
                        map_w = map_size * cell_size
                        map_h = map_size * cell_size
                        margin = 20
                        offset_x = screen_w - map_w - margin
                        offset_y = margin
                        
                        # Draw Map Background (Black)
                        rc_map_bg = RECT(offset_x, offset_y, offset_x + map_w, offset_y + map_h)
                        user32.FillRect(hdc, ctypes.byref(rc_map_bg), gdi32.CreateSolidBrush(0x000000))
                        
                        # Draw Walls (Dark Green)
                        hbrush_radar_wall = gdi32.CreateSolidBrush(0x00003300)
                        for y in range(map_size):
                            for x in range(map_size):
                                if self.world_map[y][x] == 1:
                                    rc_cell = RECT(offset_x + x*cell_size, offset_y + y*cell_size, offset_x + (x+1)*cell_size, offset_y + (y+1)*cell_size)
                                    user32.FillRect(hdc, ctypes.byref(rc_cell), hbrush_radar_wall)
                                    
                        # Draw Exit (Blue)
                        rc_exit = RECT(offset_x + 6*cell_size, offset_y + 9*cell_size, offset_x + 7*cell_size, offset_y + 10*cell_size)
                        user32.FillRect(hdc, ctypes.byref(rc_exit), hbrush_blue)
                                    
                        # Draw Entities
                        for i in range(256):
                            e = amsv_block.entities[i]
                            if (e.health > 0 or e.z > 0) and i != my_id:
                                ex_grid = int(e.x / 100.0 + 8.0)
                                ey_grid = int(e.y / 100.0 + 8.0)
                                
                                if 0 <= ex_grid < 16 and 0 <= ey_grid < 16:
                                    brush = None
                                    if 61 <= i <= 90: brush = hbrush_red # Swarm
                                    elif i == 20: brush = hbrush_yellow # Keycard
                                    elif i == 182: brush = hbrush_green # Source Code
                                    elif 176 <= i <= 179: brush = hbrush_white # Boss
                                    
                                    if brush:
                                        rc_e = RECT(offset_x + ex_grid*cell_size, offset_y + ey_grid*cell_size, offset_x + (ex_grid+1)*cell_size, offset_y + (ey_grid+1)*cell_size)
                                        user32.FillRect(hdc, ctypes.byref(rc_e), brush)
                                        
                        # Draw Player (White)
                        px_grid = int(px)
                        py_grid = int(py)
                        if 0 <= px_grid < 16 and 0 <= py_grid < 16:
                            rc_p = RECT(offset_x + px_grid*cell_size, offset_y + py_grid*cell_size, offset_x + (px_grid+1)*cell_size, offset_y + (py_grid+1)*cell_size)
                            user32.FillRect(hdc, ctypes.byref(rc_p), hbrush_white)
                            
                        gdi32.DeleteObject(hbrush_radar_wall)
                        
                    user32.ReleaseDC(0, hdc)
            except Exception as e:
                pass
            time.sleep(0.016)

    def fire(self): pass
