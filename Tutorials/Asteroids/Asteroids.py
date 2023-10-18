import pygame
from pygame import MOUSEBUTTONDOWN, MOUSEMOTION, Vector2
from pygame.transform import rotozoom
import random
from pygame.mixer import Sound

asteroid_images = ['./Images/asteroid1.png',
                   './Images/asteroid2.png', './Images/asteroid3.png',]


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
        self.shoot = Sound("./Sounds/shoot.wav")

    def update(self):
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_UP]:
            self.position += self.forward
            self.drift = (self.drift + self.forward) / 1.5
        if is_key_pressed[pygame.K_LEFT]:
            self.forward = self.forward.rotate(-2)
        if is_key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(2)
        if is_key_pressed[pygame.K_SPACE] and self.can_shoot == 0:
            # Giving it Vector2(self.position) creates a new position variable for the bullets
            # without it, we are passing/updating the ships position.
            self.bullets.append(
                Bullet(Vector2(self.position), self.forward * 10))
            self.shoot.play()
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
    def __init__(self, position, size):
        self.position = Vector2(position)
        self.velocity = Vector2(random.randint(-3, 3), random.randint(-3, 3))
        self.image = pygame.image.load(asteroid_images[size])
        self.radius = self.image.get_width() // 2
        self.explode = Sound("./Sounds/explode.mp3")
        self.size = size

    def check_collision_with_asteroids(self, asteroids):
        for other in asteroids:
            if other != self:
                if self.position.distance_to(other.position) <= self.radius + other.radius:
                    # Calculate overlap distance
                    overlap = (self.radius + other.radius) - \
                        self.position.distance_to(other.position)

                    # Calculate the collision normal
                    normal = (other.position - self.position).normalize()

                    # Move the asteroids apart to avoid sticking
                    separation = overlap / 2
                    self.position -= separation * normal
                    other.position += separation * normal

                    # Calculate relative velocity
                    relative_velocity = other.velocity - self.velocity

                    # Calculate impulse
                    impulse = 2.0 * \
                        relative_velocity.dot(
                            normal) / (1 / self.radius + 1 / other.radius)

                    # Update velocities
                    self.velocity += impulse / self.radius * normal
                    other.velocity -= impulse / other.radius * normal

    def update(self):
        self.position += self.velocity
        self.check_collision_with_asteroids(asteroids)

    def draw(self, screen):
        self.position = wrap_position(self.position, screen)
        blit_rotated(self.position, self.image, self.velocity, screen)

    # Bullet collision
    # Ship collision
    def hit(self, position):
        # if the asteroids position has a distance to the bullets position that is
        # <= the radius of the asteroid, then the bullet has hit the asteroid.
        if self.position.distance_to(position) <= self.radius:
            self.explode.play()
            return True
        return False


pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Asteroids")
screen.fill((0, 0, 0))
background = pygame.image.load("./Images/space.png")
game_over = False

# Creating ship, giving it starting position
ship = Ship((screen.get_width()//2, screen.get_height()//2))

# Creating Asteroids
# Create the emtpy list of asteroids and create a loop to make them.
# Range being the number of asteroids you want to create.
asteroids = []
for i in range(3):
    posx, posy = (random.randint(0, screen.get_width()),
                  random.randint(0, screen.get_height()))
    asteroid_position = (posx, posy)
    asteroid_direction_away_from_screen_center = (
        (screen.get_width()/2 - posx) * 0.8, (screen.get_height()/2-posy)*0.8)
    asteroid_position += asteroid_direction_away_from_screen_center
    asteroids.append(
        Asteroid((asteroid_position[0], asteroid_position[1]), 0))

# Out of bounds setting container
out_of_bounds = [-150, -150, 950, 950]

# Lose screen
font = pygame.font.Font("./Fonts/AlienFont.ttf", 80)
text_loser = font.render("You Lost!", True, (255, 255, 255))
text_loser_position = ((screen.get_width() - text_loser.get_width()) //
                       2, (screen.get_height() - text_loser.get_height())//2)
# Win screen
font2 = pygame.font.Font("./Fonts/AlienFont.ttf", 80)
text_winner = font2.render("You Won!", True, (255, 255, 255))
text_winner_position = ((screen.get_width() - text_winner.get_width()) //
                        2, (screen.get_height() - text_winner.get_height())//2)
# Score display
score = 0
score_font = pygame.font.Font("./Fonts/AlienScore.ttf", 35)
score_text_position = (10, 10)

# Lives display
lives = 3
lives_font = pygame.font.Font("./Fonts/AlienScore.ttf", 35)
lives_text_position = (10, 50)
life_timer = 0

# Quit button
quit_font = pygame.font.Font("./Fonts/AlienFont.ttf", 50)
quit_hovered = False
quit_text = quit_font.render(
    'Quit?', True, ((255, 255, 255) if quit_hovered == False else (0, 0, 0)))
quit_text_rect = quit_text.get_rect()
quit_text_rect.center = ((screen.get_width(
) - quit_text.get_width()) // 2, (screen.get_height() - text_loser.get_height()) // 2 + 100,)


clock = pygame.time.Clock()
quitting = False
running = True
winner = False
loser = False
while quitting == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            quitting = True

        if event.type == MOUSEMOTION:
            x, y = event.pos
            # Quit
            if quit_text_rect.collidepoint(x, y):
                quit_hovered = True
            else:
                quit_hovered = False

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if quit_hovered:
                game_over = True
                running = False
                quitting = True

    if running:
        while game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False
                    quitting = True

                if event.type == MOUSEMOTION:
                    x, y = event.pos
                    # Quit
                    if quit_text_rect.collidepoint(x, y):
                        quit_hovered = True
                    else:
                        quit_hovered = False

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if quit_hovered:
                        game_over = True
                        running = False
                        quitting = True

            clock.tick(55)

            # Fill screen with background image to have sprite trails cleaned up on renders.
            # It is an image that is blit to the screen.
            screen.blit(background, (0, 0))

            if ship is None:
                game_over = True
                running = False
                loser = True
                winner = False
                continue
            # if ship is None:
            #     screen.blit(text_loser, text_loser_position)
            #     screen.blit(quit_text, quit_text_rect.center)
            #     screen.blit(try_again_text, try_again_rect.center)
            #     pygame.display.update()
            #     continue

            if len(asteroids) == 0:
                game_over = True
                running = False
                winner = True
                loser = False
                continue
                # screen.blit(text_winner, text_winner_position)
                # screen.blit(quit_text, quit_text_rect.center)
                # screen.blit(try_again_text, try_again_rect.center)
                # pygame.display.update()
                # continue

            # Running ships update and draw method.
            ship.update()
            ship.draw(screen)

            # Running asteroids update and draw method.
            for asteroid in asteroids:
                asteroid.update()
                asteroid.draw(screen)
                if asteroid.hit(ship.position):
                    if lives == 0:
                        ship = None
                        break
                    elif life_timer == 0:
                        life_timer = 1500
                        lives -= 1
                        break
                    break

            # Timer for life counter so 1 asteroid wont wipe out the ships life in a second.
            if life_timer > 0:
                life_timer -= clock.get_time()
            else:
                life_timer = 0

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
                    # if a hits b then a and b need to be destroyed.
                    if asteroid.hit(bullet.position):
                        score += 1
                        if not deadbullets.__contains__(bullet):
                            deadbullets.append(bullet)
                        if not deadasteroids.__contains__(asteroid):
                            deadasteroids.append(asteroid)

            for deadbullet in deadbullets:
                ship.bullets.remove(deadbullet)

            for deadasteroid in deadasteroids:
                if deadasteroid.size < 2:
                    asteroids.append(
                        Asteroid(deadasteroid.position, deadasteroid.size + 1))
                    asteroids.append(
                        Asteroid(deadasteroid.position, deadasteroid.size + 1))
                asteroids.remove(deadasteroid)

            # Display score
            score_text = score_font.render(
                f'Score: {score}', True, (255, 255, 255))
            screen.blit(score_text, score_text_position)
            # Display lives
            lives_text = lives_font.render(
                f'Lives: {lives}', True, (255, 255, 255))
            screen.blit(lives_text, lives_text_position)

            pygame.display.update()
    else:
        if loser:
            screen.blit(text_loser, text_loser_position)
            screen.blit(quit_text, quit_text_rect.center)
            pygame.display.update()
        elif winner:
            screen.blit(text_winner, text_winner_position)
            screen.blit(quit_text, quit_text_rect.center)
            pygame.display.update()

pygame.quit()
