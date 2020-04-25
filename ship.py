'''Class to represent player ship in alien invasion game'''
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, screen, settings):
        #Setting up graphics
        super(Ship, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Movement control booleans
        self.rightMove = False
        self.leftMove = False

        #Initialize ship to always start at center of bottom of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Store center of ship separately for movement purposes
        self.center = float(self.rect.centerx)


    def update(self):
        '''Function that updates center position of ship based on user input
        Also ensure ships will not go out of screen bounds'''
        if self.rightMove and self.rect.right < self.screen_rect.right:
            self.center += self.settings.shipSpeed
        if self.leftMove and self.rect.left > 0:
            self.center -= self.settings.shipSpeed

        #Update rect object from self.center
        self.rect.centerx = self.center

    def blitship(self):
        '''Draw ship at current location on screen'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center ship on screen'''
        self.center = self.screen_rect.centerx
