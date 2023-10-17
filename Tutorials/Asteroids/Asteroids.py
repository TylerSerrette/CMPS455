import pygame
from pygame import Vector2
from pygame.transform import rotozoom

# Ship class


class Ship:
    def __init__(self, position):
        # Position variable is a 2d vector position
        self.position = Vector2(position)
        self.image = pygame.image.load("./Images/ship.png")
        # It will always go up when pressing up, even when facing somewhere else bc y = -1
        self.forward = Vector2(0, -1)

    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
        if is_key_pressed[pygame.K_LEFT]:
            self.forward = self.forward.rotate(-1)
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)

    def draw(self, screen):
        # This is done this way to the sprite can rotate from its center point and not turn weird.
        angle = self.forward.angle_to(Vector2(0, -1))
        # angle is rotational value and 1.0 is zoom value or scale.
        rotated_surface = rotozoom(self.image, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size // 2
        screen.blit(rotated_surface, blit_position)

# Asteroid class


class Asteroid:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image = pygame.image.load("./Images/asteroid1.png")

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.position)


pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Asteroids")
screen.fill((0, 0, 0))
background = pygame.image.load("./Images/space.png")
game_over = False

# Creating ship, giving it starting position
ship = Ship((100, 700))

# Creating Asteroid1, giving it starting position
asteroid = Asteroid((300, 300))

clock = pygame.time.Clock()

while not game_over:

    clock.tick(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Fill screen with background image to have sprite trails cleaned up on renders.
    # It is an image that is blit to the screen.
    screen.blit(background, (0, 0))

    # Running ships update and draw method.
    ship.update()
    ship.draw(screen)

    # Running asteroids update and draw method.
    asteroid.update()
    asteroid.draw(screen)

    pygame.display.update()

pygame.quit()
