import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Pac-Man")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
        text_rect = text.get_rect(center=(screen_width//2, screen_height//2 - 50 + i*40))
        screen.blit(text, text_rect)

        # Draw a white rectangle around the selected option
        if i == selected_option:
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 10), 2)

    pygame.display.flip()

def start_game():
    # Placeholder for starting the actual game
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

    # Game logic goes here

    # Draw everything
    screen.fill(BLACK)

    # Draw game board

    # Draw score
    # Use pygame.font to render the score text

    # Draw lives
    # Represent lives with icons or text

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
