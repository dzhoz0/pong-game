import pygame
from config import *
from menu import Menu
from config_state import ConfigState
from game import GameState

class Pong:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Pong')
        self.state = 'menu'
        self.config = {'players': 1}  # Default to one player

    def run(self):
        clock = pygame.time.Clock()
        menu = Menu(self.screen)
        config_state = ConfigState(self.screen)
        running = True

        while running:
            if self.state == 'menu':
                pygame.mixer.music.stop()
                action = menu.handle_events()
                if action == 'quit':
                    running = False
                elif action == '1_player':
                    self.config['players'] = 1
                    self.state = 'game'
                    self.game_state = GameState(self.screen, self.config)
                elif action == '2_players':
                    self.config['players'] = 2
                    self.state = 'game'
                    self.game_state = GameState(self.screen, self.config)
                elif action == 'config_game':
                    self.state = 'config'
                menu.draw()

            elif self.state == 'config':
                pygame.mixer.music.stop()
                action = config_state.handle_events()
                if action == 'quit':
                    running = False
                elif action == 'menu':
                    self.state = 'menu'
                elif action == 'set_players':
                    self.config['players'] = config_state.get_player_count()
                config_state.draw()

            elif self.state == 'game':
                # pygame.mixer.music.stop()
                action = self.game_state.handle_events()
                if action == 'quit':
                    running = False
                elif action == 'menu':
                    self.state = 'menu'
                self.game_state.update()
                self.game_state.draw()

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

if __name__ == '__main__':
    Pong().run()