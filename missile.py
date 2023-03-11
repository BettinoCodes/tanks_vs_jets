import Pygame 

from Pygame.sprite import Sprite


class Missile(Sprite):
    """This is a class for the missile of the Warthog"""
    
    def __init__(self, ri_game):
        super().__init__()
        self.screen = ri_game.screen
        self.settings = ri_game.settings    
        self.color = Pygame.Color("Red")
        self.Rect = Pygame.Rect(0,0,8,8)
        self.rect.midtop = ri_game.screen.rect.midtop
        