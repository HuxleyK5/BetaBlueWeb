"""Entry point for Pokemon Beta Blue."""

import os
import pygame

from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, STATE_TITLE, STATE_NAME_ENTRY, STATE_TOWN
from .window import GameWindow
from .player import Player
from .map import GameMap
from .input import get_movement_vector, handle_name_input
from .assets import ensure_asset_folders, load_font


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


class Game:
    def __init__(self, root_path):
        pygame.init()
        self.root_path = root_path
        ensure_asset_folders(root_path)
        self.window = GameWindow(fullscreen=False)
        self.player = Player()
        self.game_map = GameMap()
        self.state = STATE_TITLE
        self.clock = pygame.time.Clock()
        self.title_font = load_font(72)
        self.body_font = load_font(28)
        self.small_font = load_font(20)
        self.player_name = ""

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.window.toggle_fullscreen()
                elif self.state == STATE_TITLE:
                    self.handle_title_input(event)
                elif self.state == STATE_NAME_ENTRY:
                    self.player_name = handle_name_input(event, self.player_name)
                    if event.key == pygame.K_RETURN and self.player_name.strip():
                        self.player.name = self.player_name.strip()
                        self.state = STATE_TOWN
                elif self.state == STATE_TOWN:
                    self.handle_town_input(event)
        return True

    def handle_title_input(self, event):
        if event.key == pygame.K_RETURN:
            self.state = STATE_NAME_ENTRY

    def handle_town_input(self, event):
        if self.player.moving:
            return
        keys = pygame.key.get_pressed()
        dx, dy = get_movement_vector(keys)
        if dx != 0 and dy != 0:
            return
        self.player.start_move(dx, dy, self.game_map.is_solid)

    def update(self):
        if self.player.moving:
            self.player.update()

    def draw_title_screen(self):
        self.window.screen.fill((18, 30, 84))
        title_surface = self.title_font.render("Pokemon Beta Blue", True, (255, 224, 108))
        prompt_surface = self.body_font.render("Press ENTER to Start", True, (255, 255, 255))
        self.window.screen.blit(title_surface, title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
        self.window.screen.blit(prompt_surface, prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))

    def draw_name_entry(self):
        self.window.screen.fill((12, 20, 48))
        prompt_surface = self.body_font.render("Enter Your Name:", True, (255, 255, 255))
        name_surface = self.body_font.render(self.player_name, True, (255, 255, 255))
        hint_surface = self.small_font.render("Press ENTER to confirm", True, (180, 180, 180))
        self.window.screen.blit(prompt_surface, prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
        self.window.screen.blit(name_surface, name_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        self.window.screen.blit(hint_surface, hint_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))

    def draw_town(self):
        self.window.screen.fill((0, 0, 0))
        self.game_map.draw(self.window.screen)
        self.player.draw(self.window.screen, 0, 0)
        status_bar = pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        pygame.draw.rect(self.window.screen, (10, 10, 30), status_bar)
        status_text = self.small_font.render(f"Player: {self.player.name or 'Unknown'}", True, (255, 255, 255))
        self.window.screen.blit(status_text, (10, SCREEN_HEIGHT - 32))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.window.screen.fill((0, 0, 0))
            if self.state == STATE_TITLE:
                self.draw_title_screen()
            elif self.state == STATE_NAME_ENTRY:
                self.draw_name_entry()
            elif self.state == STATE_TOWN:
                self.draw_town()

            self.window.present()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    game = Game(root)
    game.run()
