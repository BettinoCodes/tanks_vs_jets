import pygame 
from pygame.sprite import Sprite

class Bombshell(Sprite):
    """A class to manage bullets fired from the tank"""
    
    def __init__(self, ri_game):
        """Create a bullet object at the tanks current position."""
        super().__init__()
        self.screen = ri_game.screen
        self.settings = ri_game.settings 
        self.color = self.settings.bombshell_color
        
        # Create a bullet rect at (0,0) and then set the correct position.
        self.rect = pygame.Rect(0,0, self.settings.bombshell_width, 
                                self.settings.bombshell_height)
        self.rect.midtop = ri_game.tank.rect.midtop
        
        # Store the bullets position a decimal value.
        self.y = float(self.rect.y)
    
    def update(self):

        """Move the bullet up the screen."""
        # Update the decimal position of the bombshell.
        self.y -= self.settings.bombshell_speed
        # Update the rect position.
        self.rect.y = self.y
    
    def draw_bombshell(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
