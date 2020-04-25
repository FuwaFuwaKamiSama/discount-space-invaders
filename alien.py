'''Class that represents an alien in a game of Space Invaders'''
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings

        #Load graphics from file
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Automatically span alien in top left corner of window
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store current position more accurately
        self.x = float(self.rect.x)

    def blitAlien(self):
        '''Update graphics to show alien's current location'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        '''Move alien left or right'''
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''Check if alien has reached edge of game window'''
        screenRect = self.screen.get_rect()
        if self.rect.right >= screenRect.right:
            return True
        elif self.rect.left <= 0:
            return True
