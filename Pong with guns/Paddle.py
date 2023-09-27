import pygame
import math as m


screenWidth = 700
screenHeight = 500
# Set the width and height of the screen [width, height]
size = (screenWidth, screenHeight)
screen = pygame.display.set_mode(size)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)


def deg2Rad(deg):
    rad = (deg / 180.0) * m.pi
    return rad


class Paddle(pygame.sprite.Sprite):
    # This class represents a paddle. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Turret Line setters
        angRad = deg2Rad(self.gunAngle)
        self.gunTipX = self.x + self.gunLen * m.cos(angRad)
        self.gunTipY = self.y + self.gunLen * m.sin(angRad)
        pygame.draw.line(
            screen, WHITE, [self.x, self.y], [self.gunTipX, self.gunTipY], 1
        )

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y > 400:
            self.rect.y = 400
