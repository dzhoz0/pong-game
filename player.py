import pygame

class Player:
    def __init__(self, paddle, player_number):
        self.paddle = paddle
        self.player_number = player_number

    def handle_input(self, screen_height):
        keys = pygame.key.get_pressed()
        if self.player_number == 1:
            if keys[pygame.K_w]:
                self.paddle.move_up()
            if keys[pygame.K_s]:
                self.paddle.move_down(screen_height)
        else:
            if keys[pygame.K_UP]:
                self.paddle.move_up()
            if keys[pygame.K_DOWN]:
                self.paddle.move_down(screen_height)