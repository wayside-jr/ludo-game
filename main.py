import pygame, sys, random
from things import WIDTH, HEIGHT, BOX, BG, GREEN, RED, BLUE, YELLOW
from Board import ludo_board
from players import init_pawns, draw_pawns
from path import PATHS 
from move_pawn import move_pawn
from Dice import roll_dice, clicking_dice, draw_dice  
from db import init_db, save_game, list_games, load_game, delete_game  

PANEL_WIDTH = 300


BG_COLOR = (255, 192, 203)


MENU_BG_IMAGE = pygame.image.load("/home/code/Desktop/ludo-game/pngtree-ludo-gul-spill-gøy-photo-image_19080058.jpg")

def choose_color(screen, available_colors=None):
    if available_colors is None:
        available_colors = ["GREEN","RED","YELLOW","BLUE"]
    font = pygame.font.SysFont(None, 50)

    while True:
        # Draw background image
        screen_width, screen_height = screen.get_size()
        bg_scaled = pygame.transform.scale(MENU_BG_IMAGE, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))

        screen.blit(font.render("Choose your color", True, (255,255,255)), (screen_width//2-150, screen_height//4))
        button_rects = []
        spacing = 50
        box_size = 100
        for i, color in enumerate(available_colors):
            x = spacing + i*(box_size + spacing)
            y = screen_height//2 - box_size//2
            rect = pygame.Rect(x, y, box_size, box_size)
            button_rects.append((rect, color))
            pygame.draw.rect(screen, pygame.Color(color), rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                for rect, color in button_rects:
                    if rect.collidepoint(mx,my):
                        return color

def choose_human_players(screen):
    font = pygame.font.SysFont(None, 50)
    options = ["1 Player", "2 Players", "3 Players", "4 Players"]
    selected_idx = 0

    while True:
        screen_width, screen_height = screen.get_size()
        bg_scaled = pygame.transform.scale(MENU_BG_IMAGE, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))

        screen.blit(font.render("PLEASE SELECT NO. PLAYERS", True, (255,255,255)), (100, 100))
        for i, option in enumerate(options):
            color = (255,255,0) if i == selected_idx else (255,255,255)
            screen.blit(font.render(option, True, color), (200, 200 + i*70))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_idx = (selected_idx - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_idx = (selected_idx + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected_idx + 1

def choose_saved_game(screen, action="Load"):
    font = pygame.font.SysFont(None, 40)
    saved_games = list_games()
    if not saved_games:
        return None
    
    selected_idx = 0
    clock = pygame.time.Clock()

    while True:
        screen_width, screen_height = screen.get_size()
        bg_scaled = pygame.transform.scale(MENU_BG_IMAGE, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))

        title = f"{action} Saved Game"
        screen.blit(font.render(title, True, (255,255,255)), (250, 100))

        for i, game_name in enumerate(saved_games):
            color = (255,255,0) if i == selected_idx else (255,255,255)
            screen.blit(font.render(game_name, True, color), (250, 200 + i*50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_idx = (selected_idx - 1) % len(saved_games)
                elif event.key == pygame.K_DOWN:
                    selected_idx = (selected_idx + 1) % len(saved_games)
                elif event.key == pygame.K_RETURN:
                    return saved_games[selected_idx]
                elif event.key == pygame.K_ESCAPE:
                    return None
        clock.tick(30)

def main_menu():
    pygame.init()
    pygame.mixer.init()

    # Dice sound
    dice_sound = pygame.mixer.Sound("/home/code/Desktop/ludo-game/Dice Roll Sound Effect ~ Rolling dice sound [dEHqgEjNsms].mp3")
    dice_sound.set_volume(0.9)

    # Background music
    pygame.mixer.music.load("/home/code/Desktop/ludo-game/Coding Stupor ~ video game music to help you focus [yA41iunMG6A].mp3")
    pygame.mixer.music.set_volume(0.2)  
    pygame.mixer.music.play(-1)  

    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Ludo Game Menu")
    font = pygame.font.SysFont(None, 50)
    clock = pygame.time.Clock()
    init_db()

    options = ["New Game", "Load Game", "Delete Game", "Exit"]
    selected_idx = 0
    running = True

    while running:
        screen_width, screen_height = screen.get_size()
        bg_scaled = pygame.transform.scale(MENU_BG_IMAGE, (screen_width, screen_height))
        screen.blit(bg_scaled, (0, 0))

        for i, option in enumerate(options):
            color = (255,255,0) if i == selected_idx else (255,255,255)
            screen.blit(font.render(option, True, color), (250, 150 + i*70))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_idx = (selected_idx - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_idx = (selected_idx + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    choice = options[selected_idx]

                    if choice == "New Game":
                        num_humans = choose_human_players(screen)
                        available_colors = ["GREEN","RED","YELLOW","BLUE"]
                        human_colors = []
                        for _ in range(num_humans):
                            color = choose_color(screen, available_colors)
                            human_colors.append(color)
                            available_colors.remove(color)

                        pawns = init_pawns()
                        dice_number = 0
                        all_colors = ["GREEN","RED","YELLOW","BLUE"]
                        player_order = all_colors
                        current_idx = player_order.index(human_colors[0])
                        user_turn = True
                        running = False
                        game_loop(pawns, dice_number, current_idx, user_turn, human_colors, dice_sound)

                    elif choice == "Load Game":
                        selected_game = choose_saved_game(screen, "Load")
                        if selected_game:
                            state = load_game(selected_game)
                            pawns = state["pawns"]
                            dice_number = state["dice_number"]
                            current_idx = state["current_idx"]
                            user_turn = state["user_turn"]
                            human_colors = [state["user_color"]]
                            running = False
                            game_loop(pawns, dice_number, current_idx, user_turn, human_colors, dice_sound)

                    elif choice == "Delete Game":
                        selected_game = choose_saved_game(screen, "Delete")
                        if selected_game:
                            delete_game(selected_game)

                    elif choice == "Exit":
                        pygame.quit()
                        sys.exit()

        clock.tick(30)

def game_loop(pawns, dice_number, current_idx, user_turn, human_colors, dice_sound):
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Ludo 4 Players")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    all_colors = ["GREEN","RED","YELLOW","BLUE"]
    player_order = all_colors
    waiting_for_pawn_click = False
    last_message = ""

    def get_game_state():
        return {
            "pawns": pawns,
            "dice_number": dice_number,
            "current_idx": current_idx,
            "user_turn": user_turn,
            "user_color": human_colors[0]
        }

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_name = f"Game_{random.randint(1000,9999)}"
                    save_game(game_name, get_game_state())
                    last_message = f"Game saved as {game_name}"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

                current_color = player_order[current_idx]

                if user_turn and current_color in human_colors:
                    if clicking_dice(mx,my) and not waiting_for_pawn_click:
                        dice_number = roll_dice()
                        dice_sound.play()  
                        movable_pawns = [
                            p for p in pawns if p["color"] == current_color and (
                                (not p["started"] and dice_number == 6) or p["started"]
                            )
                        ]
                        if movable_pawns:
                            waiting_for_pawn_click = True
                        else:
                            if dice_number != 6:
                                current_idx = (current_idx + 1) % 4

                    elif waiting_for_pawn_click:
                        clicked = False
                        for pawn in pawns:
                            if pawn["color"] == current_color:
                                x, y = PATHS[pawn["color"]][pawn["position_index"]] if pawn["started"] else pawn["home"]
                                center_x = x * BOX + BOX // 2
                                center_y = y * BOX + BOX // 2
                                if (mx - center_x)**2 + (my - center_y)**2 <= (BOX//2)**2:
                                    reached_home, captured = move_pawn(pawn, dice_number, pawns)
                                    clicked = True
                                    waiting_for_pawn_click = False
                                    if reached_home:
                                        last_message = f"{pawn['color']} pawn reached home"
                                    elif captured:
                                        abbr = {"GREEN":"G","RED":"R","YELLOW":"Y","BLUE":"B"}
                                        last_message = f"{abbr[pawn['color']]} captured {abbr[captured['color']]}"
                                    else:
                                        last_message = ""
                                    if dice_number != 6:
                                        current_idx = (current_idx + 1) % 4
                                    break
                        if not clicked and dice_number == 6:
                            for pawn in pawns:
                                if pawn["color"] == current_color and not pawn["started"]:
                                    reached_home, captured = move_pawn(pawn, dice_number, pawns)
                                    waiting_for_pawn_click = False
                                    if reached_home:
                                        last_message = f"{pawn['color']} pawn reached home"
                                    elif captured:
                                        abbr = {"GREEN":"G","RED":"R","YELLOW":"Y","BLUE":"B"}
                                        last_message = f"{abbr[pawn['color']]} captured {abbr[captured['color']]}"
                                    else:
                                        last_message = ""
                                    break

        # COMPUTER TURN
        current_color = player_order[current_idx]
        if current_color not in human_colors:
            pygame.time.delay(500)
            dice_number = roll_dice()
            my_pawns = [p for p in pawns if p["color"] == current_color]
            started_pawns = [p for p in my_pawns if p["started"]]
            base_pawns = [p for p in my_pawns if not p["started"]]

            if dice_number == 6 and base_pawns:
                pawn_to_move = base_pawns[0]
            else:
                if started_pawns:
                    pawn_to_move = None
                    for p in started_pawns:
                        new_index = p["position_index"] + dice_number
                        captured = next((o for o in pawns if o["color"] != current_color and o["started"] and o["position_index"] == new_index), None)
                        if captured:
                            pawn_to_move = p
                            break
                    if not pawn_to_move:
                        pawn_to_move = max(started_pawns, key=lambda p: p["position_index"])
                else:
                    pawn_to_move = None

            if pawn_to_move:
                reached_home, captured = move_pawn(pawn_to_move, dice_number, pawns)
                if reached_home:
                    last_message = f"{pawn_to_move['color']} pawn reached home"
                elif captured:
                    abbr = {"GREEN":"G","RED":"R","YELLOW":"Y","BLUE":"B"}
                    last_message = f"{abbr[pawn_to_move['color']]} captured {abbr[captured['color']]}"
                else:
                    last_message = ""

            if dice_number != 6:
                current_idx = (current_idx + 1) % 4

        
        screen.fill(BG_COLOR)

        # Board surface
        board_area_width = screen_width - PANEL_WIDTH
        board_area_height = screen_height
        board_surface = pygame.Surface((WIDTH, HEIGHT))
        board_surface.fill(BG)
        ludo_board(board_surface)
        draw_pawns(board_surface, pawns, PATHS)

        # Scale board
        scale_x = board_area_width / WIDTH
        scale_y = board_area_height / HEIGHT
        scale = min(scale_x, scale_y)
        scaled_board = pygame.transform.scale(board_surface, (int(WIDTH * scale), int(HEIGHT * scale)))
        screen.blit(scaled_board, (0, 0))

        # Side panel
        pygame.draw.rect(screen, BG_COLOR, (screen_width - PANEL_WIDTH, 0, PANEL_WIDTH, screen_height))  
            
        screen.blit(font.render("Roll Dice", True, (0,0,0)), (screen_width - PANEL_WIDTH + 60,60))
        draw_dice(screen, dice_number)
        if last_message:
            screen.blit(font.render(last_message, True, (0,0,0)), (screen_width - PANEL_WIDTH + 150, 350))
        if waiting_for_pawn_click:
            screen.blit(font.render("MOVE YOUR PAWN!", True, (0,0,0)), (screen_width - PANEL_WIDTH + 20, 380))
        turn_text = f"{'Your' if current_color in human_colors else 'Computer'} Turn ({current_color})"
        screen.blit(font.render(turn_text, True, (0,0,0)), (screen_width - PANEL_WIDTH + 20, 420))

        screen.blit(font.render("Press 'S' to Save", True, (0,0,0)), (screen_width - PANEL_WIDTH + 20, 500))

        # Exit button
        exit_button = pygame.Rect(WIDTH+450, HEIGHT -55, 200, 50)
        pygame.draw.rect(screen, (200, 0, 0), exit_button)
        screen.blit(font.render("Exit", True, (255,255,255)), (WIDTH+500, HEIGHT-35))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__=="__main__":
    main_menu()
