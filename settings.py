'''Class that stores settings for alien invasion game'''

class Settings():
    def __init__(self):
        #Settings for screen
        self.screenWidth = 1600
        self.screenHeight = 900
        self.bgColor = (230, 230, 230)

        #Settings for Ship
        self.shipSpeed = 1.5
        self.ship_limit = 3

        #Settings for ship bullets
        self.bulletSpeed = 2
        self.bulletWidth = 3
        self.bulletHeight = 15
        self.bulletColor = (60, 60, 60)
        self.maxBullets = 3

        #Settings for alien fleet
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        #Settings for game level-up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change as game is played'''
        self.shipSpeed = 1.5
        self.bulletSpeed = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed of game'''
        self.shipSpeed *= self.speedup_scale
        self.bulletSpeed *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
