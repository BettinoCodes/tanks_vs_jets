class GameStats:
    """Track statistics for jet Invasion."""
    def __init__(self, ri_game):
        """initialize statistics"""
        self.settings = ri_game.settings
        self.reset_stats()
        
        #Start the jet Invasion in an active state.
        self.game_active = False
        
        #High scores should not reset
        self.high_score = 0
        
    def reset_stats(self):
        """Initializen statistics that can change during the game."""
        self.tanks_left = self.settings.tank_limit
        self.score = 0
        self.level = 1
        