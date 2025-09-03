import pygame
from things import BOX, GREEN, RED, YELLOW, BLUE, WHITE, BLACK

def draw_star(screen, x, y, size, color):
    """Draw a 5-pointed star centered at (x, y)."""
    points = []
    for i in range(10):
        angle = i * 36  # 360 / 10
        radius = size if i % 2 == 0 else size // 2
        vec = pygame.math.Vector2(radius, 0).rotate(angle)
        points.append((x + vec.x, y + vec.y))
    pygame.draw.polygon(screen, color, points)

def ludo_board(screen):
    BOX = 40  # your box size

    # --- Green home ---
    pygame.draw.rect(screen, GREEN, (0, 0, 6*BOX, 6*BOX))        
    pygame.draw.rect(screen, WHITE, (BOX, BOX, 4*BOX, 4*BOX))  

    # --- Red home ---
    pygame.draw.rect(screen, RED, (9*BOX, 0, 6*BOX, 6*BOX))        
    pygame.draw.rect(screen, WHITE, (10*BOX, BOX, 4*BOX, 4*BOX))

    # --- Yellow home ---
    pygame.draw.rect(screen, YELLOW, (0, 9*BOX, 6*BOX, 6*BOX))        
    pygame.draw.rect(screen, WHITE, (BOX, 10*BOX, 4*BOX, 4*BOX))

    # --- Blue home ---
    pygame.draw.rect(screen, BLUE, (9*BOX, 9*BOX, 6*BOX, 6*BOX))        
    pygame.draw.rect(screen, WHITE, (10*BOX, 10*BOX, 4*BOX, 4*BOX))

    # --- Center triangles (finishing zone) ---
    pygame.draw.polygon(screen, GREEN, [(6*BOX, 6*BOX), (9*BOX, 6*BOX), (7.5*BOX, 7.5*BOX)])
    pygame.draw.polygon(screen, RED, [(9*BOX, 6*BOX), (9*BOX, 9*BOX), (7.5*BOX, 7.5*BOX)])
    pygame.draw.polygon(screen, YELLOW, [(6*BOX, 9*BOX), (9*BOX, 9*BOX), (7.5*BOX, 7.5*BOX)])
    pygame.draw.polygon(screen, BLUE, [(6*BOX, 6*BOX), (6*BOX, 9*BOX), (7.5*BOX, 7.5*BOX)])

    # --- Draw grid lines for playable area (excluding homes + center 3x3 square) ---
    for i in range(15):
        for j in range(15):
            # Skip colored home squares
            if (i < 6 and j < 6) or (i >= 9 and j < 6) or (i < 6 and j >= 9) or (i >= 9 and j >= 9):
                continue
            # Skip center 3x3 finishing area
            if 6 <= i <= 8 and 6 <= j <= 8:
                continue
            # Draw square outline
            pygame.draw.rect(screen, BLACK, (i*BOX, j*BOX, BOX, BOX), 1)

    # --- Safe path coloring ---
    for i in range(1, 6):
        # Green path
        pygame.draw.rect(screen, RED, (7*BOX, i*BOX, BOX, BOX))
        pygame.draw.rect(screen, BLACK, (7*BOX, i*BOX, BOX, BOX), 1)

        # Red path
        pygame.draw.rect(screen, BLUE, ((14-i)*BOX, 7*BOX, BOX, BOX))
        pygame.draw.rect(screen, BLACK, ((14-i)*BOX, 7*BOX, BOX, BOX), 1)

        # Yellow path
        pygame.draw.rect(screen, YELLOW, (7*BOX, (14-i)*BOX, BOX, BOX))
        pygame.draw.rect(screen, BLACK, (7*BOX, (14-i)*BOX, BOX, BOX), 1)

        # Blue path
        pygame.draw.rect(screen, GREEN, (i*BOX, 7*BOX, BOX, BOX))
        pygame.draw.rect(screen, BLACK, (i*BOX, 7*BOX, BOX, BOX), 1)

    # --- Connect homes to paths ---
    pygame.draw.rect(screen, GREEN, (1*BOX, 6*BOX, BOX, BOX))   # Green exit
    pygame.draw.rect(screen, RED,   (8*BOX, 1*BOX, BOX, BOX))   # Red exit
    pygame.draw.rect(screen, YELLOW,(6*BOX, 13*BOX, BOX, BOX))  # Yellow exit
    pygame.draw.rect(screen, BLUE,  (13*BOX, 8*BOX, BOX, BOX))  # Blue exit

    # --- Safe zone stars ---
    star_size = BOX // 3
    draw_star(screen, 8*BOX + BOX//2, 1*BOX + BOX//2, star_size, BLACK)   # Green path star
    draw_star(screen, 13*BOX + BOX//2, 8*BOX + BOX//2, star_size, BLACK)  # Red path star
    draw_star(screen, 6*BOX + BOX//2, 13*BOX + BOX//2, star_size, BLACK)  # Yellow path star
    draw_star(screen, 1*BOX + BOX//2, 6*BOX + BOX//2, star_size, BLACK)   # Blue path star
