import pygame
import random

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.hit_sound = pygame.mixer.Sound("assets/sfx/ball_hit.mp3")

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def check_collision(self, screen_height):
        # Collision with top and bottom walls
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.hit_sound.play()
            self.speed_y = -self.speed_y

    def check_collision_paddles(self, paddle1, paddle2):
        def circle_rect_collision(circle_x, circle_y, circle_radius, rect):
            closest_x = max(rect.left, min(circle_x, rect.right))
            closest_y = max(rect.top, min(circle_y, rect.bottom))
            distance_x = circle_x - closest_x
            distance_y = circle_y - closest_y
            return (distance_x ** 2 + distance_y ** 2) < (circle_radius ** 2)

        # Collision with paddle1
        if self.speed_x < 0 and circle_rect_collision(self.x - self.radius, self.y, self.radius, paddle1.rect):
            self.hit_sound.play()
            self.speed_x = -self.speed_x
        # Collision with paddle2
        elif self.speed_x > 0 and circle_rect_collision(self.x + self.radius, self.y, self.radius, paddle2.rect):
            self.hit_sound.play()
            self.speed_x = -self.speed_x

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)