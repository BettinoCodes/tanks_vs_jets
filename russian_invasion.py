import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from button import Button
from tank import Tank
from jet import Jet
from warthog import Warthog
from bombshell import Bombshell
from scoreboard import Scoreboard


class RussianInvasion:
    """overall to manage game assets and behavior."""

    def __init__(self):
        """Initialize, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Russian Invasion")

        # Create an instance to store statistics and score
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.tank = Tank(self)
        self.bombshells = pygame.sprite.Group()
        self.jets = pygame.sprite.Group()
        self.warthog = Warthog(self)
        self._create_fleet()

        # Create the button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.tank.update()
                self._update_bombshells()
                self._update_jets()
            self._update_screen()

    # watch for keyboard and mouse events
    # HELPER METHOD
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            # Reset the game stat first
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_tank()

            # get rid of any remrining jets and bullets
            self.jets.empty()
            self.bombshells.empty()

            # creat3 new fleet and center the tank
            self._create_fleet()
            self.tank.center_tank()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keyboard presses"""
        if event.key == pygame.K_RIGHT:
            self.tank.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.tank.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bombshell()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.tank.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.tank.moving_left = False

    def _create_fleet(self):
        """Create the fleet of jets"""
        # Create an jet and find the number of jets that fit
        # Spacing each jet with equal space in between
        jet = Jet(self)
        jet_width, jet_height = jet.rect.size
        available_space_x = self.settings.screen_width - (2 * jet_width)
        number_jets_x = available_space_x // (2*jet_width)

        # Determine the number of rows that fit on the screen
        tank_height = self.tank.rect.height
        available_space_y = (self.settings.screen_height -
                             (3*jet_height) - tank_height)
        number_rows = available_space_y // (2*jet_height)

        # Create the first fleet of jets
        for row_number in range(number_rows):
            for jet_number in range(number_jets_x):
                self._create_jet(jet_number, row_number)

    def _check_fleet_edges(self):
        """Respond if any jets have reached an edge"""
        for jet in self.jets.sprites():
            if jet.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        """drop the entire fleet and change its direction"""
        for jet in self.jets.sprites():
            jet.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_jet(self, jet_number, row_number):
        # Create an jet and place it in the row
        jet = Jet(self)
        jet_width, jet_height = jet.rect.size
        jet.x = jet_width + 2 * jet_width * jet_number
        jet.rect.x = jet.x
        jet.rect.y = jet.rect.height + 2 * jet.rect.height * row_number
        self.jets.add(jet)

    def _update_jets(self):
        """check if the jet is at the eadge, and then
        update the positions of all jets in the fleet"""
        self._check_fleet_edges()
        self.jets.update()

        # Look for jet-tank collisions
        if pygame.sprite.spritecollideany(self.tank, self.jets):
            self._tank_hit()

        # Look for jets hitting the bottom of the screen
        self._check_jets_bottom()

    def _check_jets_bottom(self):
        """check if any jets have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for jet in self.jets.sprites():
            if jet.rect.bottom >= screen_rect.bottom:
                # Treat this the same as tank hit
                self._tank_hit()
                break

    def _fire_bombshell(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bombshells) < self.settings.bombshells_allowed:
            new_bombshell = Bombshell(self)
            self.bombshells.add(new_bombshell)

    def _update_bombshells(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bombshell positions
        # Get rid of bombshell that have dissappeared
        self.bombshells.update()

        for bombshell in self.bombshells.copy():
            if bombshell.rect.bottom <= 0:
                self.bombshells.remove(bombshell)

        self._check_bombshell_jet_collisions()

    def _check_bombshell_jet_collisions(self):
        # Check for any bullets that have hit jets.
        # If so, get rid of the bullet and the jet.
        collisions = pygame.sprite.groupcollide(
            self.bombshells, self.jets, True, True)

        if collisions:
            for jets in collisions.values():
                self.stats.score += self.settings.jet_points * len(jets)
            self.sb.prep_score()
            self.sb._check_high_score()

        if not self.jets:
            # Destroy existing bombshells and create new fleet.
            self.bombshells.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _tank_hit(self):
        """Respond to the tank being hit by an jet"""
        if self.stats.tanks_left > 0:
            # decrement tanks left, update the scoreboard
            self.stats.tanks_left -= 1
            self.sb.prep_tank()
            # get rid of any remrining jets and bombshells.
            self.jets.empty()
            self.bombshells.empty()

            # Create new fleet and the center tank
            self._create_fleet()
            self.tank.center_tank()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.tank.blitme()
        for bombshell in self.bombshells.sprites():
            bombshell.draw_bombshell()
        self.jets.draw(self.screen)

        # draw the scoreboard
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        # make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance and run the game.
    ri = RussianInvasion()
    ri.run_game()
