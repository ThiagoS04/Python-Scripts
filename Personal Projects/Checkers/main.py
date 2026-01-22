"""
    Thiago Schuck 25 February 2025
    This is a checkers game that implements a GUI
    This is the main file that runs the game

"""

import Player
import Piece
import Board
import random
import pygame

def main():
    
    # Declare variables
    screen_x = 960
    screen_y = 960
    players = []

    # Initialize pygame
    pygame.init()

    title_screen(screen_x, screen_y)   # Create title screen

    
    player_info = startup(screen_x, screen_y)  # Create startup screen and get player information

    # Create board
    board = Board.Board()

    # Create player objects
    for key in player_info.keys():
        
        color = player_info[key][0]
        name = player_info[key][1]
        player = Player.Player(color, name)
        players.append(player)

    # Run game
    run_game(screen_x, screen_y, players)   # Create game loop

    pygame.quit()



"""
    Method to run game
    :param screen_x: width of screen
    :param screen_y: height of screen
    :return: None
"""
def run_game(screen_x: int, screen_y: int, players: list) -> None:

    # Declare variables
    dragging = False        # True if piece is being dragged
    offset_x = 0            # X difference between mouse and piece
    offset_y = 0            # Y difference between mouse and piece

    # Create clock
    clock = pygame.time.Clock()
    delta_time = 0.1

    # Set up the game window
    screen = pygame.display.set_mode((screen_x, screen_y))

    board = pygame.image.load("Images/board.png").convert()

    black_piece = pygame.image.load("Images/black_piece.png").convert()
    black_piece = pygame.transform.scale(black_piece, 
                        (black_piece.get_width() * 0.5, black_piece.get_height() * 0.5))   # Scale image to half size
    black_piece.set_colorkey((255, 255, 255))    # Remove white background
    piece_hitbox = pygame.Rect(0, screen_y//8, black_piece.get_width(), black_piece.get_height())   # Create hitbox for piece

    # Create game loop
    game_running = True
    while game_running:

        screen.blit(board, (0, 0))                      # Put board on screen
        screen.blit(black_piece, piece_hitbox)          # Put piece on screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:      # Mouse button pressed
                if piece_hitbox.collidepoint(event.pos):    # Mouse over piece
                    dragging = True
                    offset_x = event.pos[0] - piece_hitbox.x
                    offset_y = event.pos[1] - piece_hitbox.y

            elif event.type == pygame.MOUSEBUTTONUP:        # Mouse button released
                dragging = False

            elif event.type == pygame.MOUSEMOTION:              # Mouse moved
                if dragging:                                    # Change piece position if dragging
                    piece_hitbox.x = event.pos[0] - offset_x
                    piece_hitbox.y = event.pos[1] - offset_y

        # Display images on screen
        pygame.display.flip()

        # Advance clock
        delta_time = clock.tick(60) / 1000
        delta_time = max (0.001, min(0.1, delta_time)) # Clamp delta_time to 0.001 and 0.1



"""
    Method to create title screen
    :param screen_x: width of screen
    :param screen_y: height of screen
    :return: None
"""
def title_screen(screen_x: int, screen_y: int) -> None:

    # Set up title game window
    title_screen = pygame.display.set_mode((screen_x, screen_x))

    # Create GUI components
    title_font = pygame.font.Font(None, 100)
    title_font.set_bold(True)
    title_font.set_italic(True)
    title_text = title_font.render("Checkers", True, (255, 255, 255))

    start_button_font = pygame.font.Font(None, 70)
    start_button_font.set_bold(True)
    start_button_text = start_button_font.render("Start", True, (0, 0, 0))

    quit_button_font = pygame.font.Font(None, 50)
    quit_button_font.set_bold(True)
    quit_button_text = quit_button_font.render("Quit", True, (0, 0, 0))

    # Create buttons
    start_dim = (250, 100)
    quit_dim = (170, 60)
    start_pos = ((screen_x - start_dim[0]) / 2, screen_y / 3 - 5)
    quit_pos = ((screen_x - quit_dim[0]) / 2, screen_y / 2 - 15)
    start_button = pygame.Rect(start_pos[0], start_pos[1], start_dim[0], start_dim[1])
    quit_button = pygame.Rect(quit_pos[0], quit_pos[1], quit_dim[0], quit_dim[1])

    # Create start menu loop
    title_running = True
    while title_running:

        mpos = pygame.mouse.get_pos()    # Get mouse position
        start_collision = start_button.collidepoint(mpos)   # Check if mouse is over start button
        quit_collision = quit_button.collidepoint(mpos)     # Check if mouse is over quit button

        # Create background
        title_screen.fill((0, 0, 0))
        title_screen.blit(title_text, (300, 150))   # Put title on screen

        pygame.draw.rect(title_screen, (255, 255, 255), start_button)   # Create start button
        pygame.draw.rect(title_screen, (255, 255, 255), quit_button)     # Create quit button

        # Change button color if mouse is over it
        if start_collision:
            pygame.draw.rect(title_screen, (45, 205, 50), start_button) # Change start button color
        if quit_collision:
            pygame.draw.rect(title_screen, (205, 45, 45), quit_button)  # Change quit button color

        title_screen.blit(start_button_text, (start_pos[0] + start_dim[0] / 4, start_pos[1] + start_dim[1] / 4))
        title_screen.blit(quit_button_text, (quit_pos[0] + quit_dim[0] / 4, quit_pos[1] + quit_dim[1] / 4))

        # Handle events
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:        # Mouse button pressed
                if quit_button.collidepoint(event.pos):     # Quit button pressed
                    exit()

                elif start_button.collidepoint(event.pos):   # Start button pressed
                    title_running = False

        # Display images on screen
        pygame.display.flip()



""" 
    Method to create startup screen
    :param screen_x: width of screen
    :param screen_y: height of screen
    :return: dict with player information   {Player number: [color, name]}
"""
def startup(screen_x: int, screen_y: int) -> dict:

    # Player information
    player1_color = ""
    player2_color = ""
    player1_name = ""
    player2_name = ""

    # Set up startup game window
    startup_screen = pygame.display.set_mode((screen_x, screen_x))

    # Create texts
    player1_name_font = pygame.font.Font(None, 75)
    player1_name_font.set_italic(True)
    player1_name_text = player1_name_font.render("Player 1 name:", True, (255, 255, 255))
    player1_name_size = player1_name_text.get_size()

    player2_name_font = pygame.font.Font(None, 75)
    player2_name_font.set_italic(True)
    player2_name_text = player2_name_font.render("Player 2 name:", True, (255, 255, 255))
    player2_name_size = player2_name_text.get_size()

    choose_color_font = pygame.font.Font(None, 75)
    choose_color_font.set_italic(True)
    choose_color_text = choose_color_font.render("Choose player one color", True, (255, 255, 255))
    color_size = choose_color_text.get_size()

    red_font = pygame.font.Font(None, 25)
    red_font.set_bold(True)

    black_font = pygame.font.Font(None, 25)
    black_font.set_bold(True)

    random_font = pygame.font.Font(None, 25)
    random_font.set_bold(True)

    quit_button_font = pygame.font.Font(None, 25)
    quit_button_font.set_bold(True)

    start_button_font = pygame.font.Font(None, 50)
    start_button_font.set_bold(True)

    # Create text boxes

    
    # Create buttons
    button_dim = (105, 40)
    one_player_pos = ((screen_x - 2 * button_dim[0]) / 3, screen_y / 4)
    two_player_pos = (3 * (screen_x - 2 * button_dim[0]) / 4, screen_y / 4)
    quit_dim = (85, 40)
    quit_pos = (10, screen_y - quit_dim[1] - 60)
    start_dim = (210, 80)

    one_player_button = pygame.Rect(one_player_pos[0], one_player_pos[1], button_dim[0], button_dim[1])
    two_player_button = pygame.Rect(two_player_pos[0], two_player_pos[1], button_dim[0], button_dim[1])
    quit_button = pygame.Rect(quit_pos[0], quit_pos[1], quit_dim[0], quit_dim[1])
    red_button = pygame.Rect(one_player_pos[0], screen_y / 2, button_dim[0], button_dim[1])
    black_button = pygame.Rect((screen_y - button_dim[0]) / 2, screen_y / 2, button_dim[0], button_dim[1])
    random_button = pygame.Rect(two_player_pos[0], screen_y / 2, button_dim[0], button_dim[1])
    start_button = pygame.Rect((screen_x - start_dim[0]) / 2, screen_y - start_dim[1] - 200, start_dim[0], start_dim[1])

    # Create start menu loop
    startup_running = True
    while startup_running:

        # Detect collisions
        mpos = pygame.mouse.get_pos()                                 # Get mouse position
        quit_collision = quit_button.collidepoint(mpos)               # over quit button
        red_collision = red_button.collidepoint(mpos)                 # over red button
        black_collision = black_button.collidepoint(mpos)             # over black button
        random_collision = random_button.collidepoint(mpos)           # over random button
        start_collision = start_button.collidepoint(mpos)             # over start button

        # Create background
        startup_screen.fill((0, 0, 0))
        startup_screen.blit(choose_color_text, ((screen_x - color_size[0]) / 2, 330))

        # Render texts
        if player1_color != "RED": red_text = red_font.render("Red", True, (0, 0, 0))
        if player1_color != "BLACK": black_text = black_font.render("Black", True, (0, 0, 0))
        if player1_color != "RANDOM": random_text = random_font.render("Random", True, (0, 0, 0))

        start_button_text = start_button_font.render("Start", True, (0, 0, 0))
        quit_button_text = quit_button_font.render("Quit", True, (0, 0, 0))

        # Create buttons
        pygame.draw.rect(startup_screen, (190, 190, 190), one_player_button)   # One player button
        pygame.draw.rect(startup_screen, (190, 190, 190), two_player_button)   # Two player button
        pygame.draw.rect(startup_screen, (190, 190, 190), quit_button)         # Quit button
        pygame.draw.rect(startup_screen, (190, 190, 190), red_button)          # Red button
        pygame.draw.rect(startup_screen, (190, 190, 190), black_button)        # Black button
        pygame.draw.rect(startup_screen, (190, 190, 190), random_button)       # Random button
        pygame.draw.rect(startup_screen, (190, 190, 190), start_button)        # Start button

        # Change colors if mouse is over button
        if quit_collision:                                                                      # Quit button
            quit_button_text = quit_button_font.render("Quit", True, (0, 0, 0)) 
            pygame.draw.rect(startup_screen, (205, 45, 45), quit_button)

        if start_collision:                                                                     # Start button
            start_button_text = start_button_font.render("Start", True, (0, 0, 0))
            pygame.draw.rect(startup_screen, (45, 205, 50), start_button)

        if red_collision:                                                                        # Red button
            red_text = red_font.render("Red", True, (205, 45, 45))

        if black_collision:                                                                      # Black button
            black_text = black_font.render("Black", True, (205, 45, 45))

        if random_collision:                                                                    # Random button
            random_text = random_font.render("Random", True, (205, 45, 45))

        # Put texts on screen
        startup_screen.blit(quit_button_text, (quit_button.x + quit_dim[0] / 4, quit_button.y + quit_dim[1] / 4))
        startup_screen.blit(red_text, (red_button.x + button_dim[0] / 4, red_button.y + button_dim[1] / 4))
        startup_screen.blit(black_text, (black_button.x + button_dim[0] / 4, black_button.y + button_dim[1] / 4))
        startup_screen.blit(random_text, (random_button.x + button_dim[0] / 4, random_button.y + button_dim[1] / 4))
        startup_screen.blit(start_button_text, (start_button.x + start_dim[0] / 4, start_button.y + start_dim[1] / 4))

        # Handle events
        for event in pygame.event.get(): 

            if event.type == pygame.MOUSEBUTTONDOWN:        # Mouse button pressed
                if quit_button.collidepoint(event.pos):     # Quit button pressed
                    exit()

                elif red_button.collidepoint(event.pos):          # Red button pressed
                    player1_color = "RED"

                elif black_button.collidepoint(event.pos):        # Black button pressed
                    player1_color = "BLACK"

                elif random_button.collidepoint(event.pos):       # Random button pressed
                    player1_color = "RANDOM"

                elif start_button.collidepoint(event.pos):       # Start button pressed
                    if player1_name != "" and player2_name != "" and player1_color != "":        # If all choices made
                        startup_running = False

        # Display images on screen
        pygame.display.flip() 

    if player1_color == "RANDOM":      # Random color
        player1_color = random.choice(["RED", "BLACK"])

    if player1_color == "RED":       # If player 1 is red, player 2 is black
        player2_color = "BLACK"
    else:                           # If player 1 is black, player 2 is red
        player2_color = "RED"

    # Return player information
    return {
        "ONE": [player1_color, player1_name],
        "TWO": [player2_color, player2_name]
    }



if __name__ == "__main__":
    main()

