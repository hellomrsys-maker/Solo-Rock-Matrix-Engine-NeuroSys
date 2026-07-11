import threading
import time
import math
from infrastructure.nerve_base import NerveBase
from infrastructure.amsv import amsv_block
from infrastructure.world_map import is_wall, is_exit, unlock_door

class CAIN_000_PlayerPhysics(NerveBase):
    """
    PLAYER PHYSICS NERVE (Raycaster Edition)
    Applies WASD inputs and enforces Wall Collision.
    """
    NERVE_ID = "CAIN_000"
    DEPARTMENT = "CAIN"
    DIVISION = "instruction_routing"
    PIPELINE = "runtime"
    WIRE_COLOR = "purple"
    
    def __init__(self):
        super().__init__()
        self.physics_thread = threading.Thread(target=self._physics_loop, daemon=True)
        self.physics_thread.start()

    def _physics_loop(self):
        print("[CAIN_000] Dual-Player Physics Node ACTIVE (With Wall Collision).")
        speed = 10.0
        
        W_KEY = 1 << 0
        A_KEY = 1 << 1
        S_KEY = 1 << 2
        D_KEY = 1 << 3
        
        
        import time
        last_shot = 0.0
        last_e_toggle = 0.0
        # Spawn Keycard once
        amsv_block.entities[20].x = -700.0
        amsv_block.entities[20].y = -700.0
        amsv_block.entities[20].z = 200 # Active
        
        # --- CAIN PHYSICS MAIN LOOP ---
        while True:
            if amsv_block.state == 5:
                kb = amsv_block.keyboard_state
                if (kb & (1 << 7)) != 0: # Enter Key
                    amsv_block.state = 0
                time.sleep(0.016)
                continue
                
            # Player 1 Physics
            me = amsv_block.entities[0]
            kb = amsv_block.keyboard_state
            keycard = amsv_block.entities[20]
            
            # Check Win State
            if is_exit(me.x, me.y):
                if amsv_block.state == 4:
                    amsv_block.state = 2 # 2 = WIN
                
            # Phase 16: Source Code Key Pickup
            src_key = amsv_block.entities[182]
            if src_key.z > 0 and me.health > 0:
                dist = math.sqrt((me.x - src_key.x)**2 + (me.y - src_key.y)**2)
                if dist < 50.0:
                    src_key.z = 0
                    amsv_block.state = 4 # 4 = Extraction Protocol
                    print("SOURCE CODE KEY ACQUIRED! EXTRACTION PROTOCOL ENGAGED!")
                    
            # Keycard Pickup
            if keycard.z > 0 and me.health > 0:
                dist = math.sqrt((me.x - keycard.x)**2 + (me.y - keycard.y)**2)
                if dist < 50.0:
                    keycard.z = 0 # Hide keycard
                    amsv_block.state = 3 # 3 = Has Keycard
                    print("KEYCARD ACQUIRED!")
                    
            # Door Unlock
            if amsv_block.state == 3:
                # Door is at map_x=14, map_y=1 => x=600, y=-700
                door_dist = math.sqrt((me.x - 600)**2 + (me.y - (-700))**2)
                if door_dist < 150.0:
                    unlock_door()
                    print("DOOR UNLOCKED!")
                    
            # ATP Payload Consumption (156-165)
            for i in range(156, 166):
                atp = amsv_block.entities[i]
                if atp.z > 0 and me.health > 0:
                    dist = math.sqrt((me.x - atp.x)**2 + (me.y - atp.y)**2)
                    if dist < 30.0:
                        atp.z = 0 # Consume
                        me.health += 50.0
                        if me.health > 100.0: me.health = 100.0
                        print(f"Consumed ATP! Health: {me.health}")
            
            if me.health > 0 and amsv_block.state != 2:
                # Phase 15: Overclock Toggle
                oc = amsv_block.entities[181]
                if (kb & (1 << 6)) != 0: # E
                    if time.time() - last_e_toggle > 0.3:
                        last_e_toggle = time.time()
                        oc.z = 1.0 if oc.z == 0.0 else 0.0
                        print(f"OVERCLOCK TOGGLED: {oc.z}")
                        
                if oc.z > 0.0:
                    current_speed = 12.0
                    fire_cooldown = 0.05
                    me.health -= 0.1 # Drain Health
                    if me.health <= 0:
                        me.health = 0.1
                        oc.z = 0.0
                else:
                    current_speed = 5.0
                    fire_cooldown = 0.3
            
                if (kb & (1 << 0)) != 0: # W
                    new_x = me.x + math.cos(me.ry) * current_speed
                    new_y = me.y + math.sin(me.ry) * current_speed
                    if not is_wall(new_x, me.y): me.x = new_x
                    if not is_wall(me.x, new_y): me.y = new_y
                if (kb & (1 << 2)) != 0: # S
                    new_x = me.x - math.cos(me.ry) * current_speed
                    new_y = me.y - math.sin(me.ry) * current_speed
                    if not is_wall(new_x, me.y): me.x = new_x
                    if not is_wall(me.x, new_y): me.y = new_y
                if (kb & (1 << 1)) != 0: # A
                    me.ry -= 0.05
                if (kb & (1 << 3)) != 0: # D
                    me.ry += 0.05
                    
                # Player Firing Logic
                ms = amsv_block.mouse_state
                is_firing = (ms & (1 << 0)) != 0 or (kb & (1 << 4)) != 0
                if is_firing and time.time() - last_shot > fire_cooldown:
                    last_shot = time.time()
                    # Find free bullet slot (1 to 10)
                    for i in range(1, 11):
                        bullet = amsv_block.entities[i]
                        if bullet.z <= 0:
                            bullet.x = me.x
                            bullet.y = me.y
                            bullet.z = 200 # Active
                            bullet_speed = 20.0
                            bullet.vx = math.cos(me.ry) * bullet_speed
                            bullet.vy = math.sin(me.ry) * bullet_speed
                            break
                            
            # Player Bullet Physics (Entities 1-10)
            for i in range(1, 11):
                bullet = amsv_block.entities[i]
                if bullet.z > 0:
                    new_x = bullet.x + bullet.vx
                    new_y = bullet.y + bullet.vy
                    
                    if is_wall(new_x, new_y):
                        bullet.z = 0 # Destroy on wall
                    else:
                        bullet.x = new_x
                        bullet.y = new_y
                        
                        # Enemy Collision (Swarm 61-90)
                        for j in range(61, 91):
                            enemy = amsv_block.entities[j]
                            if enemy.z > 0:
                                dx = bullet.x - enemy.x
                                dy = bullet.y - enemy.y
                                if math.sqrt(dx*dx + dy*dy) < 30.0:
                                    bullet.z = 0
                                    enemy.z = 0 # Destroy Enemy
                                    print(f"Enemy {j} destroyed!")
                                    break
                                    
            # Phase 14: Cybernetic Hacking (EMP Override)
            if (kb & (1 << 5)) != 0: # Spacebar
                emp = amsv_block.entities[180]
                if emp.z == 0.0 and me.health > 50.0:
                    me.health -= 50.0
                    emp.z = 1.0 # Active
                    emp.health = 0.0 # Radius starts at 0
                    emp.x = me.x
                    emp.y = me.y
                    print("EMP OVERRIDE ACTIVATED!")
                        
            # Update EMP Expansion
            emp = amsv_block.entities[180]
            if emp.z > 0.0:
                emp.health += 25.0 # Expansion speed
                radius = emp.health
                
                # Check for Immune cells in radius
                immune_indices = list(range(96, 99)) + list(range(131, 136)) + list(range(176, 180))
                for idx in immune_indices:
                    cell = amsv_block.entities[idx]
                    if cell.health > 0:
                        dx = cell.x - emp.x
                        dy = cell.y - emp.y
                        if math.sqrt(dx*dx + dy*dy) < radius:
                            cell.vx = -1.0 # Paralyzed/Glitched!
                            cell.rz = 0.0 # Reset timer
                            
                if radius > 600.0:
                    emp.z = 0.0 # Stop expanding
                    
            # Enemy Laser Physics (Entities 100-130)
            for i in range(100, 130):
                laser = amsv_block.entities[i]
                if laser.z > 0:
                    new_x = laser.x + laser.vx
                    new_y = laser.y + laser.vy
                    
                    if is_wall(new_x, new_y):
                        laser.z = 0 # Destroy on wall
                    else:
                        laser.x = new_x
                        laser.y = new_y
                        
                        # Player Collision
                        if me.health > 0:
                            dx = laser.x - me.x
                            dy = laser.y - me.y
                            if math.sqrt(dx*dx + dy*dy) < 30.0:
                                laser.z = 0
                                me.health -= 5.0
                                print(f"Player hit! Health: {me.health}")
                                
            # Antibody Physics (Entities 136-150)
            for i in range(136, 151):
                antibody = amsv_block.entities[i]
                if antibody.z > 0:
                    new_x = antibody.x + antibody.vx
                    new_y = antibody.y + antibody.vy
                    
                    if is_wall(new_x, new_y):
                        antibody.z = 0 # Destroy on wall
                    else:
                        antibody.x = new_x
                        antibody.y = new_y
                        
                        # Player Collision
                        if me.health > 0:
                            dx = antibody.x - me.x
                            dy = antibody.y - me.y
                            if math.sqrt(dx*dx + dy*dy) < 30.0:
                                antibody.z = 0
                                me.health -= 10.0 # Antibodies hurt!
                                
                        # Infected Swarm Collision
                        for j in range(61, 91):
                            enemy = amsv_block.entities[j]
                            if enemy.z > 0 and enemy.vx == 1.0: # Only hits infected
                                dx = antibody.x - enemy.x
                                dy = antibody.y - enemy.y
                                if math.sqrt(dx*dx + dy*dy) < 30.0:
                                    antibody.z = 0
                                    enemy.vx = -1.0 # PARALYZED!
                                    break
            
            # PLAYER 2
            p2_in = amsv_block.controller_1
            A_KEY = 1 << 1
            D_KEY = 1 << 3
            if p2_in & A_KEY: amsv_block.entities[200].ry -= 0.05
            if p2_in & D_KEY: amsv_block.entities[200].ry += 0.05
            
            p2_x = amsv_block.entities[200].x
            p2_y = amsv_block.entities[200].y
            p2_ry = amsv_block.entities[200].ry
            
            speed = 10.0
            W_KEY = 1 << 0
            S_KEY = 1 << 2
            if p2_in & W_KEY: 
                new_x = p2_x + speed * math.cos(p2_ry)
                new_y = p2_y + speed * math.sin(p2_ry)
                if not is_wall(new_x, p2_y): amsv_block.entities[200].x = new_x
                if not is_wall(p2_x, new_y): amsv_block.entities[200].y = new_y
            if p2_in & S_KEY: 
                new_x = p2_x - speed * math.cos(p2_ry)
                new_y = p2_y - speed * math.sin(p2_ry)
                if not is_wall(new_x, p2_y): amsv_block.entities[200].x = new_x
                if not is_wall(p2_x, new_y): amsv_block.entities[200].y = new_y
            
            time.sleep(0.016)

    def fire(self): pass
