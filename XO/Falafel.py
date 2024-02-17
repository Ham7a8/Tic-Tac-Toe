# Import pygame, pygame.gfxdraw, and random modules
import pygame
import pygame.gfxdraw
import random

# Initialize pygame
pygame.init()

# Define the screen size and create the screen object
screen_size = (650, 650)
screen = pygame.display.set_mode(screen_size)

# Load the background image and scale it to fit the screen size
background = pygame.image.load("XO/bg.png")
background = pygame.transform.smoothscale(background, screen_size)

# Load the start image and adjust its transparency
start_image = pygame.image.load("XO/start.png").convert_alpha()
start_image = pygame.transform.scale(start_image, screen_size)

# Load the O and X images and store them in lists
O_images = [pygame.transform.smoothscale(pygame.image.load(f"XO/O_{i}.png").convert_alpha(), (200, 200)) for i in range(1, 6)]
X_images = [pygame.transform.smoothscale(pygame.image.load(f"XO/X_{i}.png").convert_alpha(), (200, 200)) for i in range(1, 5)]
# Define the game squares as a list of dictionaries
squares = [
    {'x': 94, 'y': 115.6, 'width': 141.9, 'height': 134.3, 'marked': False},
    {'x': 98.4, 'y': 256.2, 'width': 141.9, 'height': 116.5, 'marked': False},
    {'x': 94, 'y': 384.2, 'width': 146.3, 'height': 116.5, 'marked': False},
    {'x': 246.8, 'y': 118.1, 'width': 128.2, 'height': 129.1, 'marked': False},
    {'x': 247.9, 'y': 256.2, 'width': 127, 'height': 117.6, 'marked': False},
    {'x': 247.9, 'y': 383, 'width': 127, 'height': 117.6, 'marked': False},
    {'x': 382.6, 'y': 114, 'width': 137.9, 'height': 131.4, 'marked': False},
    {'x': 381.6, 'y': 256.2, 'width': 151.7, 'height': 119.3, 'marked': False},
    {'x': 381.6, 'y': 382.5, 'width': 152.2, 'height': 118.2, 'marked': False},
]

# Define a function to check if a square is clicked by the mouse
def is_clicked(square, mouse_pos):
    # Get the x and y coordinates of the mouse position
    mouse_x, mouse_y = mouse_pos
    # Get the x, y, width and height of the square
    square_x = square['x']
    square_y = square['y']
    square_width = square['width']
    square_height = square['height']
    # Check if the mouse position is within the square boundaries
    if square_x <= mouse_x <= square_x + square_width and square_y <= mouse_y <= square_y + square_height:
        return True
    else:
        return False

# Define a function to draw an O or X image on a square
def draw_mark(square, mark):
    # Get the x and y coordinates of the square
    square_x = square['x']
    square_y = square['y']
    # Get the index of the O or X image based on the number of marked squares
    if mark == 'O':
        image_index = sum([1 for s in squares if s['marked'] == 'O'])
        image = pygame.transform.scale(O_images[image_index], (200, 200))
    elif mark == 'X':
        image_index = sum([1 for s in squares if s['marked'] == 'X']) % len(X_images)
        image = pygame.transform.scale(X_images[image_index], (200, 200))
    # Get the width and height of the image
    image_width, image_height = image.get_size()
    # Calculate the position to center the image on the square
    image_x = square_x + (square['width'] - image_width) / 2
    image_y = square_y + (square['height'] - image_height) / 2
    # Draw the image on the screen
    screen.blit(image, (image_x, image_y))

# Define a function to check if a player has won the game
def check_win(mark):
    # Define the winning combinations as a list of lists of square indices
    win_combos = [
        [0, 1, 2], # Top row
        [3, 4, 5], # Middle row
        [6, 7, 8], # Bottom row
        [0, 3, 6], # Left column
        [1, 4, 7], # Middle column
        [2, 5, 8], # Right column
        [0, 4, 8], # Diagonal from top left to bottom right
        [2, 4, 6], # Diagonal from top right to bottom left
    ]
    # Loop through the winning combinations
    for combo in win_combos:
        # Get the squares corresponding to the combo
        square1 = squares[combo[0]]
        square2 = squares[combo[1]]
        square3 = squares[combo[2]]
        # Check if all the squares are marked by the same mark
        if square1['marked'] == mark and square2['marked'] == mark and square3['marked'] == mark:
            return True
    # If none of the winning combinations are satisfied, return False
    return False

# Define a function to check if the game is a tie
def check_tie():
    # Loop through the squares
    for square in squares:
        # If any square is not marked, return False
        if not square['marked']:
            return False
    # If all the squares are marked, return True
    return True

# Define a variable to store the current player's mark
current_mark = 'X'

# Define a variable to store the game state
game_over = False

# Define a variable to store the game result
game_result = None

# Define a variable to indicate whether the game has started
game_started = False

# Define a variable to track if the background has been blitted
background_blitted = False
hamza_font = pygame.font.Font('XO/font.otf', 40)
screen.fill((255,255,255))
startMessage = hamza_font.render("hamza", True, (0,0,0))
screen.blit(startMessage, ((screen.get_width()/2 - startMessage.get_width()/2) -10, screen.get_height()/2 - startMessage.get_height()/2))
pygame.display.update()
pygame.time.delay(2000)

# Start the main game loop
screen.blit(start_image, (0, 0))
test_font = pygame.font.Font('XO/font.otf', 80)
title_font = pygame.font.Font('XO/font.otf', 150)
title_text = title_font.render('Tic Tac Toe', True, (20, 47, 66))
title_rect = title_text.get_rect(center = (325,100))

screen.blit(title_text, title_rect)

pygame.display.update()

while True:
    # Handle the events
    for event in pygame.event.get():
        # If the user clicks the close button, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # If the user clicks the mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the game has not started and the start image is clicked
            if not game_started and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                start_rect = start_image.get_rect(topleft=(0, 0))
                # If the mouse is clicked within the start image
                if start_rect.collidepoint(mouse_pos):
                    game_started = True
            # If the game is not over and the left mouse button is clicked
            elif not game_over and event.button == 1:
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Loop through the squares
                for square in squares:
                    # If the square is clicked and not marked
                    if is_clicked(square, mouse_pos) and not square['marked']:
                        # Mark the square with the current mark
                        square['marked'] = current_mark
                        # Draw the mark on the square
                        draw_mark(square, current_mark)
                        # Check if the current player has won the game
                        if check_win(current_mark):
                            # Set the game state to over
                            game_over = True
                            # Set the game result to the current mark
                            game_result = current_mark
                        # Check if the game is a tie
                        elif check_tie():
                            # Set the game state to over
                            game_over = True
                            # Set the game result to tie
                            game_result = 'Tie'
                        # Switch the current mark to the other mark
                        else:
                            if current_mark == 'X':
                                current_mark = 'O'
                            else:
                                current_mark = 'X'
                        # Break the loop
                        break
        # If the game is over and the R key is pressed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # Reset the game
            game_over = False
            game_result = None
            current_mark = 'X'
            for square in squares:
                square['marked'] = False

    # Fill the screen with the background image if the game has started and the background hasn't been blitted
    if game_started and not background_blitted:
        screen.blit(background, (0, 0))
        background_blitted = True

    # If the game is not over and the game has started, update the display
    if game_started and not game_over:
        pygame.display.update()

    # If the game is over, display the game result
    if game_over:
        # Create a font object
        test_font = pygame.font.Font('XO/font.otf', 100)
        
        # Define text and background colors based on game result
        if game_result == 'X':
            text = test_font.render('X Wins!', True, (20, 47, 66))
            text_rect = text.get_rect(center = (325,70))
            background_color = (255, 255, 255, 128)  # Semi-transparent white
        elif game_result == 'O':
            text = test_font.render('O Wins!', True, (20, 47, 66))
            background_color = (255, 255, 255, 128)  # Semi-transparent white
            text_rect = text.get_rect(center = (325,70))
        else:
            text = test_font.render('Tie Game!', True, (20, 47, 66) )
            background_color = (255, 255, 255, 128)  # Semi-transparent white
            text_rect = text.get_rect(center = (325,70))
        # Get the width and height of the text surface
        text_width, text_height = text.get_size()


        # Draw the text on the screen
        screen.blit(text, text_rect)
    
    # Update the display
    pygame.display.update()
