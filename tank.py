import pygame
from pygame.sprite import Sprite

class Tank:
    """A class to manage the tank """
    
    
    def __init__(self, ai_game):
        """Initialize the game's settings."""
        super().__init__()
        # Screen settings
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        #load the tank image and get its rect
        self.image = pygame.image.load('images/tank.bmp')
        self.rect = self.image.get_rect()
        
        #Start each new tank at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        self.x = float(self.rect.x)
        
        # Set flag movement
        self.moving_right = False
        self.moving_left = False   
        
    def update(self):
        """update the tanks position based on the movement flag"""
        # Update the tanks x position x value, not the rect.
        
        if self.moving_right and self.rect.right < self.screen_rect.right: 
            self.x += self.settings.tank_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.tank_speed
     
        # Update the rect object from self.x.
        self.rect.x = self.x
        
    def blitme(self):
        """Draw the tank at its current location"""   
        self.screen.blit(self.image, self.rect)
        
    def center_tank(self):
        """Center the tank on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
