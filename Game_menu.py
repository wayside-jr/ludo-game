import pygame, sys
from db import init_db, list_games, load_game, delete_game
from main import main, init_pawns  # import main game functions

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ludo Game Menu")
font = pygame.font.SysFont(None, 50)
clock = pygame.time.Clock()

# Initialize database
init_db()

# --- Load background image ---
try:
    bg_image = pygame.image.load("menu_bg.jpg")
    bg_image = pygame.transform.scale(bg_image, (800, 600))
except:
    bg_image = None  # fallback if image not found

# --- Draw menu ---
def draw_menu(options, selected_idx):
    if bg_image:
        screen.blit(bg_image, (0,0))
    else:
        screen.fill((50,50,50))

    for i, option in enumerate(options):
        color = (255,255,0) if i == selected_idx else (255,255,255)
        text_surf = font.render(option, True, color)
        text_rect = text_surf.get_rect(center=(400, 200 + i*70))
        screen.blit(text_surf, text_rect)

    pygame.display.flip()

# --- Choose saved game (load or delete) ---
def choose_saved_game(action="load"):
    while True:
        if bg_image:
            screen.blit(bg_image, (0,0))
        else:
            screen.fill((50,50,50))

        title = "Load Game" if action=="load" else "Delete Game"
        screen.blit(font.render(title, True, (255,255,255)), (250,50))

        saved_games = list_games()
        if not saved_games:
            screen.blit(font.render("No saved games!", True, (255,0,0)), (250,200))
            pygame.display.flip()
            pygame.time.delay(1000)
            return None

        button_rects = []
        spacing = 20
        for i, name in enumerate(saved_games):
            rect = pygame.Rect(250, 150 + i*(50+spacing), 300, 50)
            button_rects.append((rect, name))
            pygame.draw.rect(screen, (200,200,200), rect)
            screen.blit(font.render(name, True, (0,0,0)), (rect.x+10, rect.y+10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                for rect, name in button_rects:
                    if rect.collidepoint(mx,my):
                        if action=="load":
                            return load_game(name)
                        elif action=="delete":
                            delete_game(name)
                            return None

# --- Main menu loop ---
def main_menu():
    options = ["New Game", "Load Game", "Delete Game", "Exit"]
    selected_idx = 0
    running = True

    while running:
        draw_menu(options, selected_idx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_idx = (selected_idx -1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_idx = (selected_idx +1) % len(options)
                elif event.key == pygame.K_RETURN:
                    selected_option = options[selected_idx]

                    if selected_option == "New Game":
                        pawns = init_pawns()
                        dice_number = 0
                        state = {
                            "pawns": pawns,
                            "dice_number": dice_number,
                            "current_idx": 0,
                            "user_turn": True,
                            "user_color": "GREEN"
                        }
                        running = False
                        main(state, user_color="GREEN")  # start main game

                    elif selected_option == "Load Game":
                        state = choose_saved_game("load")
                        if state:
                            running = False
                            main(state, user_color=state["user_color"])

                    elif selected_option == "Delete Game":
                        choose_saved_game("delete")

                    elif selected_option == "Exit":
                        pygame.quit()
                        sys.exit()

        clock.tick(30)

if __name__=="__main__":
    main_menu()
