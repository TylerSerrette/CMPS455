import pygame
from Ball import Ball
from Paddles import Paddle

pygame.init()

# Initials
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong With Guns")

# Colors
BLUE = (0, 0, 225)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


# Paddle stuff

# Main loop
running = True
while running:
    window.fill(BLACK)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        #
    #

    # OBJECTS
    # Ball
    duhball = Ball(window, YELLOW, WIDTH, HEIGHT)
    duhball.drawMe()

    # Paddle
    player_paddle = Paddle(window, BLUE, WIDTH, HEIGHT, "left")
    player_paddle.drawMe()
    cpu_paddle = Paddle(window, RED, WIDTH, HEIGHT, "right")
    cpu_paddle.drawMe()

    # MOVEMENTS
    for i in pygame.event.get():
        duhball.moveMe()

    pygame.display.update()
#
