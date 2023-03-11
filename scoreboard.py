import pygame.font
from pygame.sprite import Group

from tank import Tank

class Scoreboard:
    """A class to report scoring information"""
    
    def __init__(self,ai_game):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect= self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        #font settings for scoring information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        
        #Prepare the initial score image 
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_tank()
        
    def prep_tank(self):
        """show how many tanks are left"""
        self.tanks = Group()
        for tank_number in range(self.stats.tanks_left):
            tank = Tank(self.ai_game)
            tank.rect.x = 10 + tank_number * tank.rect.width
            tank.rect.y = 10
            self.tanks.add_internal(tank)
            
    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        
        #position the level below the score 
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        
    def prep_high_score(self):
        """Turn the high score into a render image"""
        high_score_str = str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        
        #center the high score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def prep_score(self): 
        """Turn the score into a rendered image"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        
        #Display
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def show_score(self):
        """Draw the score and tanks left to the board"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.tanks.draw(self.screen)
        
        
    def _check_high_score(self):
        """Check to see if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()