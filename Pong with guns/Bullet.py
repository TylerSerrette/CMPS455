import pygame as p
import math as m


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
screenWidth = 700
screenHeight = 500


s = p.display.set_mode(screenWidth, screenHeight)


class Bullet(p.sprite.Sprite):
    def __init__(self, centerx, centery):
        self.x = centerx
        self.y = centery
        self.radius = 5

        # Call the parent class (Sprite) constructor
        super().__init__()

    def deg2Rad(deg):
        rad = (deg / 180.0) * m.pi
        return rad

    def drawMe(self, s):
        if self.hit == False:
            p.draw.circle(
                s, GREEN, [int(self.x), int(self.y)], self.radius, 1)
        else:
            self.explodeMe(s)

        return

    def moveMe(self):
        angRad = self.deg2Rad(self.heading)
        bX = self.x + self.velocity * m.cos(angRad)
        bY = self.y + self.velocity * m.sin(angRad)
        if ((bX > 0) and (bX < screenWidth)) and ((bY > 0) and (bY < screenHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False
        return

    def doIExist(self):
        return self.exists

    def explodeMe(self, s):
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius - 4, 1)
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius, 1)
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius + 4, 1)
        p.draw.circle(
            s, ORANGE, [int(self.x), int(self.y)], self.radius + 6, 1)
        p.draw.circle(
            s, ORANGE, [int(self.x), int(self.y)], self.radius + 9, 1)
        p.draw.circle(
            s, YELLOW, [int(self.x), int(self.y)], self.radius + 11, 1)
        p.draw.circle(
            s, YELLOW, [int(self.x), int(self.y)], self.radius + 13, 1)

        self.hit = False
        self.exists = False
        return

    #     # Pass in the color of the paddle, its width and height.
    #     # Set the background color and set it to be transparent
    #     self.image = pygame.Surface((50, 10))
    #     self.image.fill(RED)
    #     self.image.set_colorkey(RED)
    #     self.rect = self.image.get_rect(center=(center))

    # def update(self):
    #     self.rect.x += 10
