import pygame


class Paddle:
    def __init__(self, window, border_color, screen_width, screen_height, right_or_left_paddle):
        self.window = window
        self.border_color = border_color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.paddle_width = 20
        self.paddle_height = 120
        self.paddle_ycoordinate = self.screen_height/2 - self.paddle_height/2

        if right_or_left_paddle == "left":
            self.paddle_xcoordinate = 100 - self.paddle_width/2
        elif right_or_left_paddle == "right":
            self.paddle_xcoordinate = self.screen_width - \
                (100 - self.paddle_width/2)

    #

    def drawMe(self):
        pygame.draw.rect(self.window, self.border_color, pygame.Rect(
            self.paddle_xcoordinate, self.paddle_ycoordinate, self.paddle_width, self.paddle_height))
#
