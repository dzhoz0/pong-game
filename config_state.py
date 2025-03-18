import os
import json
import pygame
from config import *

class ConfigState:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.background_options = ['None'] + self._get_files('assets/backgrounds')
        self.music_options = ['None'] + self._get_files('assets/music')
        self.color_options = ['White', 'Red', 'Green', 'Blue']
        self.selected_bg_idx = 0
        self.selected_music_idx = 0
        self.selected_color_idx = 0
        self.menu_options = ['Background: ', 'Music: ', 'Color: ', 'Save config', 'Back to menu']
        self.selected_idx = 0
        self.config_file = 'game_config.json'
        self._load_config()

    def _get_files(self, folder):
        return [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    def _load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.selected_bg_idx = self.background_options.index(data.get('background', 'None'))
                self.selected_music_idx = self.music_options.index(data.get('music', 'None'))
                self.selected_color_idx = self.color_options.index(data.get('color', 'White'))

    def _save_config(self):
        data = {
            'background': self.background_options[self.selected_bg_idx],
            'music': self.music_options[self.selected_music_idx],
            'color': self.color_options[self.selected_color_idx]
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_idx = (self.selected_idx - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_idx = (self.selected_idx + 1) % len(self.menu_options)
                elif event.key == pygame.K_LEFT:
                    if self.selected_idx == 0:
                        self.selected_bg_idx = (self.selected_bg_idx - 1) % len(self.background_options)
                    elif self.selected_idx == 1:
                        self.selected_music_idx = (self.selected_music_idx - 1) % len(self.music_options)
                    elif self.selected_idx == 2:
                        self.selected_color_idx = (self.selected_color_idx - 1) % len(self.color_options)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_idx == 0:
                        self.selected_bg_idx = (self.selected_bg_idx + 1) % len(self.background_options)
                    elif self.selected_idx == 1:
                        self.selected_music_idx = (self.selected_music_idx + 1) % len(self.music_options)
                    elif self.selected_idx == 2:
                        self.selected_color_idx = (self.selected_color_idx + 1) % len(self.color_options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_idx == 3:
                        self._save_config()
                    elif self.selected_idx == 4:
                        self._save_config()
                        return 'menu'
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_idx else (150, 150, 150)
            if i == 0:
                text = f'{option}{self.background_options[self.selected_bg_idx]}'
            elif i == 1:
                text = f'{option}{self.music_options[self.selected_music_idx]}'
            elif i == 2:
                text = f'{option}{self.color_options[self.selected_color_idx]}'
            else:
                text = option
            label = self.font.render(text, True, color)
            x = (WIDTH - label.get_width()) // 2
            y = (HEIGHT // 2) + i * 50
            self.screen.blit(label, (x, y))
        pygame.display.flip()