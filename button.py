'''Class that represents a button to be used to start/pause Space Invaders game'''
import pygame.font

class Button():
    def __init__(self, settings, screen, message):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Building button dimensions and properties and centering it
        self.width = 200
        self.height = 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(message)

    def prep_msg(self, message):
        '''Function that adds text message to button centered in button'''
        self.msg_image = self.font.render(message, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draws blank button then adds message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
