"""
    Thiago Schuck 25 February 2025
    This is a checkers game that implements a GUI
    This is the main file that runs the game

"""

import Player
import Piece
import random
import pygame

def main():
    
    # Declare variables
    name: str
    color: str
    numPlayers: int
    screen_x = 960
    screen_y = 960

    dragging = False        # True if piece is being dragged
    offset_x = 0            # X difference between mouse and piece
    offset_y = 0            # Y difference between mouse and piece

    # Initialize pygame
    pygame.init()

    # Create clock
    clock = pygame.time.Clock()
    delta_time = 0.1

    title_screen(screen_x, screen_y)   # Create title screen

    startup(screen_x, screen_y)  # Create startup screen

    # Get number of players

    # Get information to create player objects

    # Create board

    # Run game

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

    pygame.quit()



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



def startup(screen_x: int, screen_y: int) -> None:

    # Set up startup game window
    startup_screen = pygame.display.set_mode((screen_x, screen_x))

    # Create GUI components
    num_players_font = pygame.font.Font(None, 75)
    num_players_font.set_italic(True)
    num_players_text = num_players_font.render("Choose number of players", True, (255, 255, 255))

    one_player_font = pygame.font.Font(None, 25)
    one_player_font.set_bold(True)

    two_player_font = pygame.font.Font(None, 25)
    two_player_font.set_bold(True)

    quit_button_font = pygame.font.Font(None, 25)
    quit_button_font.set_bold(True)

    # Create buttons
    player_dim = (105, 40)
    one_player_pos = ((screen_x - 2 * player_dim[0]) / 3, screen_y / 4)
    two_player_pos = (3 * (screen_x - 2 * player_dim[0]) / 4, screen_y / 4)
    quit_dim = (85, 40)
    quit_pos = (10, screen_y - quit_dim[1] - 60)
    one_player_button = pygame.Rect(one_player_pos[0], one_player_pos[1], player_dim[0], player_dim[1])
    two_player_button = pygame.Rect(two_player_pos[0], two_player_pos[1], player_dim[0], player_dim[1])
    quit_button = pygame.Rect(quit_pos[0], quit_pos[1], quit_dim[0], quit_dim[1])

    # Create start menu loop
    startup_running = True
    while startup_running:

        mpos = pygame.mouse.get_pos()    # Get mouse position
        one_player_collision = one_player_button.collidepoint(mpos)   # Check if mouse is over start button
        two_player_collision = two_player_button.collidepoint(mpos)   # Check if mouse is over quit button
        quit_collision = quit_button.collidepoint(mpos)     # Check if mouse is over quit button

        # Create background
        startup_screen.fill((0, 0, 0))
        startup_screen.blit(num_players_text, (150, 90))

        one_player_text = one_player_font.render("1 Player", True, (255, 255, 255))
        two_player_text = two_player_font.render("2 Player", True, (255, 255, 255))
        quit_button_text = quit_button_font.render("Quit", True, (255, 255, 255))

        pygame.draw.rect(startup_screen, (0, 0, 0), one_player_button)   # Create one player button
        pygame.draw.rect(startup_screen, (0, 0, 0), two_player_button)   # Create two player button
        pygame.draw.rect(startup_screen, (0, 0, 0), quit_button)     # Create quit button

        # Change colors if mouse is over button
        if one_player_collision:                                                               # One player button
            one_player_text = one_player_font.render("1 Player", True, (45, 205, 50))
        if two_player_collision:                                                                # Two player button
            two_player_text = two_player_font.render("2 Player", True, (45, 205, 50))
        if quit_collision:                                                                      # Quit button
            quit_button_text = quit_button_font.render("Quit", True, (0, 0, 0)) 
            pygame.draw.rect(startup_screen, (205, 45, 45), quit_button)

        startup_screen.blit(one_player_text, (one_player_pos[0] + player_dim[0] / 4, one_player_pos[1] + player_dim[1] / 4))
        startup_screen.blit(two_player_text, (two_player_pos[0] + player_dim[0] / 4, two_player_pos[1] + player_dim[1] / 4))
        startup_screen.blit(quit_button_text, (quit_pos[0] + quit_dim[0] / 4, quit_pos[1] + quit_dim[1] / 4))

        # Handle events
        for event in pygame.event.get(): 

            if event.type == pygame.MOUSEBUTTONDOWN:        # Mouse button pressed
                if quit_button.collidepoint(event.pos):     # Quit button pressed
                    exit()

                elif one_player_button.collidepoint(event.pos):   # One player button pressed
                    pass

                elif two_player_button.collidepoint(event.pos):   # Two player button pressed
                    pass

        # Display images on screen
        pygame.display.flip() 



""" 
    Method to get and verify number of players playing
    :return: number of players
"""
def getNumPlayers() -> int:

    validNumberOfPlayers = False
    while not validNumberOfPlayers: 
        try:
            # Ask user for number of players
            numplayers = int(input("How many people are playing?\t"))

            # Check if input is valid
            if numplayers < 1 or numplayers > 2:
                raise ValueError("Number of players must be 1 or 2.")
            
            validNumberOfPlayers = True

        # Catch any errors and print error message
        except ValueError as e:
            print(f"Error: {e}, please try again.")
            continue

    return numplayers



"""
    Method to get and verify player color
    Allows user to randomly assign color or choose their own
    :return: player color
"""
def getPlayerColor() -> str:

    # Ask if user wants a random color
    chooseRandom = randomColor()

    if chooseRandom:
        color = random.choice(["black", "white"])
        print(f"Your color is {color}.")
        return color

    validColor = False
    while not validColor:
        # Ask user for color choice
        color = input("What color do you want to be?\t").strip().lower()

        # Check if input is valid
        if color not in ["black", "white"]:
            print("Please choose black or white.")
            continue



"""
    Method to choose random color
    :return: booleaning if player chose color or not
"""
def randomColor() -> bool:

    validChoice = False
    while not validChoice:
        # Ask if player wants to choose color
        chooseColor = input("Do you want to choose your color?\t").strip().lower()

        # Check if input is valid
        if chooseColor not in ["yes", "no"]:
            print("Please answer yes or no.")
            continue
        
        if chooseColor == "yes":    # Let player choose color
            return False

        else:                       # Randomly assign color
            return True



"""
    Method to get user name
    :return: user name
"""
def getPlayerName() -> str:

    validName = False
    while not validName:
        # Ask for user name
        name = input("What is your name?\t")

        # Check if input is valid
        if len(name) < 1:
            print("Name cannot be empty.")
            continue

        validName = True

    return name




if __name__ == "__main__":
    main()

