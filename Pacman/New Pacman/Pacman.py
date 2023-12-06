import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 681, 744
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Pac-Man")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load the board background
board_background = pygame.image.load('./Images/Other/Board.png')

# Load the sprite sheet
# sprite_sheet = pygame.image.load('./Images/Arcade-Pac-Man-GeneralSprites.png')

# # Function to extract sprites from the sprite sheet
# def get_sprite(x, y, width, height, sprites_file):
#     """ Extracts and returns a sprite from the sprite sheet """
#     sprite = pygame.Surface((width, height))
#     sprite.blit(sprites_file, (0, 0), (x, y, width, height))
#     sprite.set_colorkey(BLACK)  # Assuming black is the transparent color
#     return sprite


# # Define the sprites based on their positions in the sprite sheet
# # Replace x, y, width, height with actual values
# pacman_sprite = get_sprite(x, y, width, height, sprites_file)

# Define game entities using the sprites


class PacMan(pygame.sprite.Sprite):
    # Your PacMan class code here
    pass


class Ghost(pygame.sprite.Sprite):
    # Your Ghost class code here
    pass

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./Images/Other/Vitamin.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./Images/Other/PowerUp.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Constants for the layout
ITEM_SPACING = 20  # Space between items
POWERUP_SPACING = ITEM_SPACING * 4  # Space from the corner for the powerup

# Constants for the game
ITEM_SIZE = 10  # The size of the item
POWERUP_SIZE = 30  # The size of the power-up

# Function to create a grid of item positions
def create_item_grid(width, height, spacing):
    return [(x, y) for x in range(spacing, width - spacing, spacing) 
                  for y in range(spacing, height - spacing, spacing)]

# Function to find corner positions for power-ups
def corner_positions(width, height, spacing):
    return [(spacing, spacing), (width - spacing - 30, spacing),
            (spacing, height - spacing - 30), (width - spacing - 30, height - spacing - 30)]
    
# Function to check if a position is valid for placing an item or power-up
def is_valid_position(x, y, board, item_size):
    # Check if the position is within the bounds of the board paths
    # This is a simplified check, you will need to check against your actual board layout
    if board.get_at((x, y)) != (0, 0, 255, 255):  # Assuming blue walls are pure blue (0, 0, 255)
        # Check if the entire item can fit without overlapping walls
        for i in range(item_size):
            for j in range(item_size):
                if board.get_at((x+i, y+j)) == (0, 0, 255, 255):
                    return False
        return True
    return False

# Function to create a grid of valid item positions
def create_valid_positions(board, item_size, spacing):
    valid_positions = []
    for x in range(0, screen_width, spacing):
        for y in range(0, screen_height, spacing):
            if is_valid_position(x, y, board, item_size):
                valid_positions.append((x, y))
    return valid_positions

# Use the function to get valid positions
item_positions = create_valid_positions(board_background, ITEM_SIZE, ITEM_SIZE)
powerup_positions = create_valid_positions(board_background, POWERUP_SIZE, POWERUP_SIZE * 3)

# Now filter the powerup_positions to only keep the strategic positions you want
# For example, the corners, or specific positions you determine manually

# Create the items and power-ups
items = pygame.sprite.Group()
powerups = pygame.sprite.Group()

for pos in item_positions:
    items.add(Item(pos[0], pos[1]))

# Assuming you have determined your power-up positions manually
# for pos in powerup_positions:
#     powerups.add(PowerUp(pos[0], pos[1]))

# In the main game loop, draw these items and power-ups just like before


for pos in item_positions:
    # You may want to add a condition to check if the position is actually on a pathway
    items.add(Item(pos[0], pos[1]))

for pos in powerup_positions:
    powerups.add(PowerUp(pos[0], pos[1]))

# Game variables
score = 0
lives = 3
menu_options = ['Start Game', 'Quit Game']
selected_option = 0

# Font
font = pygame.font.Font(None, 36)


def show_menu(selected_option):
    screen.fill(BLACK)
    for i, option in enumerate(menu_options):
        text = font.render(option, True, WHITE)
        text_rect = text.get_rect(
            center=(screen_width//2, screen_height//2 - 50 + i*40))
        screen.blit(text, text_rect)

        # Draw a white rectangle around the selected option
        if i == selected_option:
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 10), 2)

    pygame.display.flip()


def start_game():
    # Placeholder for starting the actual game
    screen.blit(board_background, (0, 0))
    pygame.display.flip()

    print("Game Started")
    return False  # Exit menu


def quit_game():
    pygame.quit()
    sys.exit()


def handle_menu_selection(selected_option):
    if selected_option == 0:
        return start_game()
    elif selected_option == 1:
        quit_game()


# Menu loop
in_menu = True
while in_menu:
    show_menu(selected_option)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                in_menu = handle_menu_selection(selected_option)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()



    # Game logic goes here


    # Draw game board
    screen.blit(board_background, (0, 0))  # Draw the background

    # Draw score
    # Use pygame.font to render the score text
    
        # Draw items and power-ups
    items.draw(screen)
    powerups.draw(screen)

    # Draw lives
    # Represent lives with icons or text

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
