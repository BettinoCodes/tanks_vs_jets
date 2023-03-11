import pygame
from pygame.sprite import Sprite


class Jet(Sprite):
    """Making a single jet"""
    
    def __init__(self, ri_game):
        """Initialize the jetand set its starting positions"""
        super().__init__()
        self.screen = ri_game.screen
        self.settings = ri_game.settings
        
        # Load the jetimage and set the rect attributes
        self.image = pygame.image.load('images/jet.bmp')
        self.rect = self.image.get_rect()
        
        #Start each new jetnear the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #store the jets exact horizontal position
        self.x = float(self.rect.x)
        
    def update(self):
        """Move the jet to the right or left"""
        self.x += (self.settings.jet_speed*self.settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        """Return True if an jetis at the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True