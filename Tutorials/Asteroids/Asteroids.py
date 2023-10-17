import pygame
from pygame import Vector2
from pygame.transform import rotozoom
import random


def blit_rotated(position, image, forward, screen):
    # This is done this way to the sprite can rotate from its center point and not turn weird.
    angle = forward.angle_to(Vector2(0, -1))
    # angle is rotational value and 1.0 is zoom value or scale.
    # rotozoom helps make the center of the ship the pivot point
    rotated_surface = rotozoom(image, angle, 1.0)
    rotated_surface_size = Vector2(rotated_surface.get_size())
    blit_position = position - rotated_surface_size // 2
    screen.blit(rotated_surface, blit_position)

# If you go off the screen by say 3px, what this does is it divides by the whole screen length
# which will give you a remainder of those 3px at the bottom of the screen.


def wrap_position(position, screen):
    x, y = position
    w, h = screen.get_size()
    return Vector2(x % w, y % h)


# Ship class


class Ship:
    def __init__(self, position):
        # Position variable is a 2d vector position
        self.position = Vector2(position)
        self.image = pygame.image.load("./Images/ship.png")
        # It will always go up when pressing up, even when facing somewhere else bc y = -1
        self.forward = Vector2(0, -1)
        self.bullets = []
        self.can_shoot = 0
        self.drift = (0, 0)

    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
            self.drift = (self.drift + self.forward) / 1.5
        if is_key_pressed[pygame.K_LEFT]:
            self.forward = self.forward.rotate(-1)
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)
        if is_key_pressed[pygame.K_SPACE] and self.can_shoot == 0:
            # Giving it Vector2(self.position) creates a new position variable for the bullets
            # without it, we are passing/updating the ships position.
            self.bullets.append(
                Bullet(Vector2(self.position), self.forward * 10))
            # can_shoot = 500ms
            self.can_shoot = 500

        # Basically the timer to count down if we can shoot.
        # We use clock.get_time() because it's a global value that can help keep track of our time.
        if self.can_shoot > 0:
            self.can_shoot -= clock.get_time()
        else:
            self.can_shoot = 0

        self.position += self.drift

    def draw(self, screen):
        self.position = wrap_position(self.position, screen)
        blit_rotated(self.position, self.image, self.forward, screen)


# Bullet class
class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position += self.velocity

    def draw(self, screen):
        # Draw a rectangle bullet.
        # The rectangle is drawn on the screen, it is red,
        # and its rectangle is self.position.x, self.position.y and it will be 5x5
        pygame.draw.rect(screen, (255, 0, 0), [
                         self.position.x, self.position.y, 5, 5])


# Asteroid class


class Asteroid:
    def __init__(self, position):
        self.position = Vector2(position)
        self.velocity = Vector2(random.randint(-3, 3), random.randint(-3, 3))
        self.image = pygame.image.load("./Images/asteroid1.png")
        self.radius = self.image.get_width() // 2

    def update(self):
        self.position += self.velocity

    def draw(self, screen):
        self.position = wrap_position(self.position, screen)
        blit_rotated(self.position, self.image, self.velocity, screen)

    # Bullet collision
    # Ship collision
    def hit(self, position):
        # if the asteroids position has a distance to the bullets position that is
        # <= the radius of the asteroid, then the bullet has hit the asteroid.
        if self.position.distance_to(position) <= self.radius:
            return True
        return False


pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Asteroids")
screen.fill((0, 0, 0))
background = pygame.image.load("./Images/space.png")
game_over = False

# Creating ship, giving it starting position
ship = Ship((100, 700))

# Creating Asteroids
# Create the emtpy list of asteroids and create a loop to make them.
# Range being the number of asteroids you want to create.
asteroids = []
for i in range(10):
    # Asteroids appear in random positions on the screen.
    asteroids.append(Asteroid((random.randint
                               (0, screen.get_width()), random.randint(0, screen.get_height()))))

# Out of bounds setting container
out_of_bounds = [-150, -150, 950, 950]

clock = pygame.time.Clock()

while not game_over:

    clock.tick(55)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Fill screen with background image to have sprite trails cleaned up on renders.
    # It is an image that is blit to the screen.
    screen.blit(background, (0, 0))

    if ship is None:
        pygame.display.update()
        continue

    # Running ships update and draw method.
    ship.update()
    ship.draw(screen)

    # Running asteroids update and draw method.
    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw(screen)
        if asteroid.hit(ship.position):
            ship = None
            break

    if ship is None:
        continue

    deadbullets = []
    deadasteroids = []

    # Running bullets update and draw method.
    for bullet in ship.bullets:
        bullet.update()
        bullet.draw(screen)

        # If bullet goes out of bounds it gets put in dead bullet list
        if bullet.position.x < out_of_bounds[0] or \
            bullet.position.x > out_of_bounds[2] or \
                bullet.position.y < out_of_bounds[1] or \
        bullet.position.y > out_of_bounds[3]:
            if not deadbullets.__contains__(bullet):
                deadbullets.append(bullet)

        for asteroid in asteroids:
            # if a hits b then a and be need to be destroyed.
            if asteroid.hit(bullet.position):
                if not deadbullets.__contains__(bullet):
                    deadbullets.append(bullet)
                if not deadasteroids.__contains__(asteroid):
                    deadasteroids.append(asteroid)

    for deadbullet in deadbullets:
        ship.bullets.remove(deadbullet)

    for deadasteroid in deadasteroids:
        asteroids.remove(deadasteroid)

    pygame.display.update()

pygame.quit()
