import pygame, random
from things import WIDTH, HEIGHT

# --- Dice constants ---
PANEL_WIDTH = 250
DICE_SIZE = 100
DICE_X = WIDTH + 500  # side panel left offset
DICE_Y = 200          # top offset for dice in panel

def roll_dice():
    """Return a random dice number 1–6"""
    return random.randint(1,6)

def clicking_dice(mx, my):
    """Return True if mouse clicked inside dice"""
    rect = pygame.Rect(DICE_X, DICE_Y, DICE_SIZE, DICE_SIZE)
    return rect.collidepoint(mx, my)

def draw_dice(screen, number):
    """Draw dice square and dots"""
    # Draw dice square
    pygame.draw.rect(screen, (255, 255, 255), (DICE_X, DICE_Y, DICE_SIZE, DICE_SIZE))
    pygame.draw.rect(screen, (0,0,0), (DICE_X, DICE_Y, DICE_SIZE, DICE_SIZE), 3)

    if number == 0:
        return  # don't draw dots yet

    # Coordinates for dots
    cx = DICE_X + DICE_SIZE//2
    cy = DICE_Y + DICE_SIZE//2
    offset = DICE_SIZE//4
    radius = 10

    def pip(x, y):
        pygame.draw.circle(screen, (0,0,0), (x,y), radius)

    if number == 1:
        pip(cx, cy)
    elif number == 2:
        pip(cx - offset, cy - offset)
        pip(cx + offset, cy + offset)
    elif number == 3:
        pip(cx - offset, cy - offset)
        pip(cx, cy)
        pip(cx + offset, cy + offset)
    elif number == 4:
        pip(cx - offset, cy - offset)
        pip(cx + offset, cy - offset)
        pip(cx - offset, cy + offset)
        pip(cx + offset, cy + offset)
    elif number == 5:
        pip(cx - offset, cy - offset)
        pip(cx + offset, cy - offset)
        pip(cx - offset, cy + offset)
        pip(cx + offset, cy + offset)
        pip(cx, cy)
    elif number == 6:
        pip(cx - offset, cy - offset)
        pip(cx, cy - offset)
        pip(cx + offset, cy - offset)
        pip(cx - offset, cy + offset)
        pip(cx, cy + offset)
        pip(cx + offset, cy + offset)
