'''File to be used to actually launch and run Space Invaders game'''
import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    '''Setting up game window and game elements'''
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screenWidth, game_settings.screenHeight))
    pygame.display.set_caption("Discount Space Invaders")
    playerShip = Ship(screen, game_settings)
    aliens = Group()
    gf.create_fleet(game_settings, screen, playerShip, aliens)
    bullets = Group() #store bullets in a group
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, screen, stats)
    play_button = Button(game_settings, screen, "Play")

    #Start up screen with blank background and play button
    gf.update_screen(game_settings, screen, playerShip, bullets, aliens, stats, play_button, sb)

    '''Game will continue to run until user inputs a QUIT command'''
    while True:
        #Check for player input
        gf.check_events(game_settings, screen, playerShip, bullets, stats, play_button, aliens, sb)
        #Update screen to latest gamestate
        if stats.game_active:
            playerShip.update()
            gf.update_bullets(aliens, bullets, game_settings, screen, playerShip, stats, sb)
            gf.update_aliens(game_settings, aliens, playerShip, stats, screen, bullets, sb)
            gf.update_screen(game_settings, screen, playerShip, bullets, aliens, stats, play_button, sb)

run_game()
