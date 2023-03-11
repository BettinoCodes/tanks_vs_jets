import pygame


class Warthog:
    """A class to manage the warthog """

    def __init__(self, ai_game):
        """This is the class for the warthog"""
    

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.screen_rect = ai_game.screen.get_rect()

        # load the warthog image and get its rect
        self.image = pygame.image.load('images/warthog.bmp')
        self.rect = self.image.get_rect()

        # Start each new warthog at the bottom center of the screen
        self.rect.midtop = self.screen_rect.midtop

    def update(self):
        """Move the warthog to the right or left"""
        self.x += (self.settings.warthog_speed*self.settings.wdirection)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if an warthog is at the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def blitme(self):
        """Draw the warthog at its current location"""
        self.screen.blit(self.image, self.rect)
