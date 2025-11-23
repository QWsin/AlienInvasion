import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from game_stats import GameStats
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    def __init__(self):
        pygame.init() # let pygame initialize its background
        self.game_active = False


        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # this is a surface, in pygame every element is a surface
        # after every loop this surface will be redrawn

        if self.settings.mode=='windowed':
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        elif self.settings.mode=='fullscreen':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            raise ValueError(f"Unknown mode in settings.mode: {self.settings.mode}")

        pygame.display.set_caption("Alien Invasion")
        self.play_button = Button(self, "Play")
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.scoreboard = Scoreboard(self)
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()
                self.clock.tick(self.settings.fps)  # limit to 60 frames per second

    def _update_aliens(self):
        if self._check_alien_edges():
            self._change_alien_fleet_direction()
        self.aliens.update()
        if self._check_aliens_bottom() or pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                return True

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            self._reset_game()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _reset_game(self):
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()

    def _check_alien_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                return True
        return False

    def _change_alien_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullets_aliens_collisions()

    def _check_bullets_aliens_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if collisions:
            sum = 0
            for v in collisions.values():
                sum += len(v)
            self.stats.score += self.settings.alien_points * sum
            self.scoreboard.check_high_score()
            self.scoreboard.prep_score()
        if len(self.aliens) == 0:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

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
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self._start_game()

    def _start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.game_active = True
        self._reset_game()
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.game_active:
            self._start_game()

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(new_bullet)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _create_fleet(self):
        alien=Alien(self)
        current_y = alien.rect.height
        while current_y + 2*alien.rect.height < self.ship.rect.top:
            current_x = alien.rect.width
            while current_x + 2*alien.rect.width < self.settings.screen_width:
                new_alien = Alien(self)
                new_alien.rect.x = current_x
                new_alien.rect.y = current_y
                new_alien.x = float(new_alien.rect.x)
                self.aliens.add(new_alien)
                current_x += 2 * alien.rect.width
            current_y += 2 * alien.rect.height

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.scoreboard.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()