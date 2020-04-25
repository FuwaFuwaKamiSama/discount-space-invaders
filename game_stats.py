'''Class that keeps track of key game statistics and updates them as needed'''

class GameStats():
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        '''Function that generates initial blank stats to updated in game'''
        self.shipsLeft = self.settings.ship_limit
        self.score = 0
        self.level = 1
