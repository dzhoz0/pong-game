class Bot:
    def __init__(self, paddle):
        self.paddle = paddle

    def move_paddle_up(self):
        self.paddle.move_up()

    def move_paddle_down(self, screen_height):
        self.paddle.move_down(screen_height)