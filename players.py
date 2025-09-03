import pygame
from things import BOX, GREEN, RED, BLUE, YELLOW


OFFSETS = {
    "GREEN": [(-21,-21),(-14,-21),(-21,-14),(-14,-14)],
    "RED":   [(-21,-21),(-14,-21),(-21,-14),(-14,-14)],
    "YELLOW":[(-21,-21),(-14,-21),(-21,-14),(-14,-14)],
    "BLUE":  [(-21,-21),(-14,-21),(-21,-14),(-14,-14)]
}

COLOR_MAP = {
    "GREEN": GREEN,
    "RED": RED,
    "YELLOW": YELLOW,
    "BLUE": BLUE
}

def init_pawns():
    return [
        {"color": "GREEN", "position_index": 0, "started": False, "home": (2, 2)},
        {"color": "GREEN", "position_index": 0, "started": False, "home": (4, 2)},
        {"color": "GREEN", "position_index": 0, "started": False, "home": (2, 4)},
        {"color": "GREEN", "position_index": 0, "started": False, "home": (4, 4)},

        {"color": "RED", "position_index": 0, "started": False, "home": (11, 2)},
        {"color": "RED", "position_index": 0, "started": False, "home": (13, 2)},
        {"color": "RED", "position_index": 0, "started": False, "home": (11, 4)},
        {"color": "RED", "position_index": 0, "started": False, "home": (13, 4)},

        {"color": "YELLOW", "position_index": 0, "started": False, "home": (2, 11)},
        {"color": "YELLOW", "position_index": 0, "started": False, "home": (4, 11)},
        {"color": "YELLOW", "position_index": 0, "started": False, "home": (2, 13)},
        {"color": "YELLOW", "position_index": 0, "started": False, "home": (4, 13)},

        {"color": "BLUE", "position_index": 0, "started": False, "home": (11, 11)},
        {"color": "BLUE", "position_index": 0, "started": False, "home": (13, 11)},
        {"color": "BLUE", "position_index": 0, "started": False, "home": (11, 13)},
        {"color": "BLUE", "position_index": 0, "started": False, "home": (13, 13)},
    ]

def draw_single_pawn(screen, color, pos, offset=(0,0)):
    x, y = pos
    dx, dy = offset
    center_x = x * BOX + BOX//2 + dx
    center_y = y * BOX + BOX//2 + dy

    
    pygame.draw.circle(screen, (0,0,0), (center_x, center_y), BOX//3+2)  # outline
    pygame.draw.circle(screen, color, (center_x, center_y), BOX//3)

def draw_pawns(screen, pawns, paths):
    for i, pawn in enumerate(pawns):
        if pawn.get("started", False):
            
            pos = paths[pawn["color"]][pawn["position_index"]]
            offset = (0,0)
        else:
            
            pos = pawn["home"]
            color_offsets = OFFSETS[pawn["color"]]
            offset = color_offsets[i%4]  

        draw_single_pawn(screen, COLOR_MAP[pawn["color"]], pos, offset)
