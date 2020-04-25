'''Class that models a bullet fired from a ship in a space invaders knockoff'''

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen

        #Generate bullet and set correct position afterwards
        self.rect = pygame.Rect(0, 0, settings.bulletWidth, settings.bulletHeight)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #Store bullet's vertical position as decimal
        self.y = float(self.rect.y)

        #Miscellaneous settings like color and speed
        self.color = settings.bulletColor
        self.speed = settings.bulletSpeed

    def update(self):
        '''Update position of bullet as it travels up the screen'''
        self.y -= self.speed
        self.rect.y = self.y

    def drawBullet(self):
        '''Draws the bullet on the screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)
