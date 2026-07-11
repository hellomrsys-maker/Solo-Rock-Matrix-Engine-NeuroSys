# 16x16 World Map 
# 0 = Empty Space
# 1 = Wall
# 2 = Exit Zone (Win Condition)
# 3 = Locked Door
# 4 = Glucose Rich Zone (Nutrients)
# 5 = Oxygen Rich Zone (Vascular)
# Grid spacing: Each tile represents 100x100 physical coordinates.
# Center of map (8, 8) corresponds to (0, 0) physical coordinates.

WORLD_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,5,5,0,1,0,0,0,1,4,4,0,1,1,3,1],
    [1,5,1,0,1,0,1,0,1,0,1,0,0,0,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,1,1,1,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,4,4,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,0,5,5,1],
    [1,4,4,0,0,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,1,0,1,1,1,1,1,1,0,1,0,1],
    [1,1,1,0,1,0,0,0,5,5,5,1,0,1,0,1],
    [1,0,0,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,4,4,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,5,5,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

def is_wall(phys_x, phys_y):
    """
    Given a physical coordinate, returns True if it's a wall or locked door.
    """
    map_x = int(phys_x / 100.0) + 8
    map_y = int(phys_y / 100.0) + 8
    
    if map_x < 0 or map_x >= 16 or map_y < 0 or map_y >= 16:
        return True # Out of bounds is a wall
        
    val = WORLD_MAP[map_y][map_x]
    return val == 1 or val == 3

def is_exit(phys_x, phys_y):
    map_x = int(phys_x / 100.0) + 8
    map_y = int(phys_y / 100.0) + 8
    if map_x < 0 or map_x >= 16 or map_y < 0 or map_y >= 16: return False
    return WORLD_MAP[map_y][map_x] == 2

def is_glucose_zone(phys_x, phys_y):
    map_x = int(phys_x / 100.0) + 8
    map_y = int(phys_y / 100.0) + 8
    if map_x < 0 or map_x >= 16 or map_y < 0 or map_y >= 16: return False
    return WORLD_MAP[map_y][map_x] == 4

def is_oxygen_zone(phys_x, phys_y):
    map_x = int(phys_x / 100.0) + 8
    map_y = int(phys_y / 100.0) + 8
    if map_x < 0 or map_x >= 16 or map_y < 0 or map_y >= 16: return False
    return WORLD_MAP[map_y][map_x] == 5

def unlock_door():
    for y in range(16):
        for x in range(16):
            if WORLD_MAP[y][x] == 3:
                WORLD_MAP[y][x] = 0
