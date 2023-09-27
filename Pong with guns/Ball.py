import pygame


class Ball:

    def __init__(self, window, color, screen_width, screen_height):
        self.window = window
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.radius = 15
        self.center_xcoordinate = self.screen_width / 2 - self.radius
        self.center_ycoordinate = self.screen_height / 2 - self.radius

        self.ball_velocity_x, self.ball_velocity_y = 0.7, 0.7
        # self.center_xcoordinate += self.ball_velocity_x
        # self.center_ycoordinate += self.ball_velocity_y
    #

    # Draw the ball
    def drawMe(self):
        pygame.draw.circle(self.window, self.color,
                           (self.center_xcoordinate, self.center_ycoordinate), self.radius)
        #
    #

    def moveMe(self):
        self.center_xcoordinate += self.ball_velocity_x
        self.center_ycoordinate += self.ball_velocity_y
    #
#
