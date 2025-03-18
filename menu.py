import pygame
from config import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["1 Player", "2 Players", "Config game", "Quit"]
        self.selected_idx = 0
        self.font = pygame.font.SysFont("Arial", 36)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, text in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_idx else (150, 150, 150)
            label = self.font.render(text, True, color)
            x = (WIDTH - label.get_width()) // 2
            y = (HEIGHT // 2) + i * 50
            self.screen.blit(label, (x, y))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_idx = (self.selected_idx - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_idx = (self.selected_idx + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_idx].lower().replace(" ", "_")
        return None

