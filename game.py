import pygame
import random
from paddle import Paddle
from ball import Ball
from player import Player
from bot import Bot
import json

class GameState:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.font = pygame.font.SysFont('Arial', 36)
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.paddle_width = 20
        self.paddle_height = 100
        self.ball_radius = 15
        self.ball_speed_x = 7
        self.ball_speed_y = 7
        self.score1 = 0
        self.score2 = 0
        self.max_score = 10
        self.game_over = False
        self.winner = None
        self.win_sound = pygame.mixer.Sound("assets/sfx/win_sound.mp3")
        self.init_game()

    def init_game(self):
        self.paddle1 = Paddle(30, (self.height - self.paddle_height) // 2, self.paddle_width, self.paddle_height, 20)
        self.paddle2 = Paddle(self.width - 50, (self.height - self.paddle_height) // 2, self.paddle_width, self.paddle_height, 20)
        self.ball = Ball(self.width // 2, self.height // 2, self.ball_radius, self.ball_speed_x, self.ball_speed_y)
        self.player1 = Player(self.paddle1, 1)
        self.player2 = Player(self.paddle2, 2) if self.config['players'] == 2 else Bot(self.paddle2)

        configGame = self.load_game_config()
        self.text_color = self.get_color_from_config(configGame.get('color', 'White'))
        if configGame['music'] != 'None':
            pygame.mixer.music.load(configGame['music'])
            pygame.mixer.music.play(-1)

    def load_game_config(self, file_path='game_config.json'):
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config

    def get_color_from_config(self, color_name):
        colors = {
            'White': (255, 255, 255),
            'Red': (255, 0, 0),
            'Green': (0, 255, 0),
            'Blue': (0, 0, 255)
        }
        return colors.get(color_name, (255, 255, 255))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_RETURN:
                    return 'menu'
        return None

    def update(self):
        if not self.game_over:
            self.player1.handle_input(self.height)
            if isinstance(self.player2, Player):
                self.player2.handle_input(self.height)
            else:
                pass
                # self.update_bot()

            self.ball.move()
            self.ball.check_collision(self.height)
            self.ball.check_collision_paddles(self.paddle1, self.paddle2)

            if self.ball.x - self.ball.radius <= 0:
                self.score2 += 1
                self.reset_ball()
            elif self.ball.x + self.ball.radius >= self.width:
                self.score1 += 1
                self.reset_ball()

            if self.score1 >= self.max_score or self.score2 >= self.max_score:
                self.game_over = True
                self.winner = 'Player 1' if self.score1 >= self.max_score else 'Player 2'
                self.win_sound.play()

    def update_bot(self):
        if self.ball.y < self.paddle2.rect.y:
            self.paddle2.move_up()
        elif self.ball.y > self.paddle2.rect.y + self.paddle2.rect.height:
            self.paddle2.move_down(self.height)

    def reset_ball(self):
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2
        self.ball.speed_x = random.choice([-7, 7])
        self.ball.speed_y = random.choice([-7, 7])

    def draw(self):
        configurations = self.load_game_config()
        background_image_path = configurations.get('background', None)

        if background_image_path and background_image_path != 'None':
            background_image = pygame.image.load(background_image_path)
            self.screen.blit(background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        self.paddle1.draw(self.screen)
        self.paddle2.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_scoreboard()

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_scoreboard(self):
        score_text = f'{self.score1} - {self.score2}'
        label = self.font.render(score_text, True, self.text_color)
        x = (self.width - label.get_width()) // 2
        y = 20
        self.screen.blit(label, (x, y))

    def draw_game_over(self):
        game_over_text = f'{self.winner} wins! Press Enter to return to menu'
        label = self.font.render(game_over_text, True, self.text_color)
        x = (self.width - label.get_width()) // 2
        y = self.height // 2
        self.screen.blit(label, (x, y))