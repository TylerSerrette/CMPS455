# Import the pygame library and initialise the game engine
import pygame
from OldPaddle import Paddle
from Bullet import Bullet

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

player_paddle = Paddle(WHITE, 10, 100)
player_paddle.rect.x = 20
player_paddle.rect.y = 200

cpu_paddle = Paddle(WHITE, 10, 100)
cpu_paddle.rect.x = 670
cpu_paddle.rect.y = 200

# This will be groups that will contain all the sprites we intend to use in our game.
paddle_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

# Add the paddles to the list of sprites
paddle_group.add(player_paddle)
paddle_group.add(cpu_paddle)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                carryOn = False

    # Moving the paddles when the user uses the arrow keys (player A) or "W/S" keys (player B)
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     cpu_paddle.moveUp(5)
    # if keys[pygame.K_s]:
    #     cpu_paddle.moveDown(5)
    if keys[pygame.K_UP]:
        player_paddle.moveUp(5)
    if keys[pygame.K_DOWN]:
        player_paddle.moveDown(5)
    if keys[pygame.K_SPACE]:
        bullet = player_paddle.shoot()
        if bullet:
            bullet_group.add(bullet)

    # --- Game logic should go here
    paddle_group.update()
    bullet_group.update()

    # --- Drawing code should go here
    # First, clear the screen to black.
    screen.fill(BLACK)
    # Draw the net
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

    # Draw all the sprites in one go.
    paddle_group.draw(screen)
    bullet_group.draw(screen)

    # Update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
