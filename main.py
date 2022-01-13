import pygame
import os
import sys

FPS = 30
ball_sprite_grup = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_board():
    boar_image = load_image('Board.png')
    screen.blit(boar_image, (1, 1))


def draw_ball():
    ball_sprite_grup_draw = pygame.sprite.Group()
    ball_sprite = pygame.sprite.Sprite()
    ball_sprite.image = load_image("Ball.png")
    ball_sprite.rect = ball_sprite.image.get_rect()

    for x in range(3):
        for y in range(2):
            ball_sprite.rect.x = 388 + x * 84
            ball_sprite.rect.y = 53 + y * 84
            ball_sprite_grup_draw.add(ball_sprite)
            ball_sprite_grup.add(ball_sprite)
            ball_sprite_grup_draw.draw(screen)

    for x in range(3):
        for y in range(3):
            ball_sprite.rect.x = 217 + x * 85
            ball_sprite.rect.y = 223 + y * 84
            ball_sprite_grup_draw.add(ball_sprite)
            ball_sprite_grup.add(ball_sprite)
            ball_sprite_grup_draw.draw(screen)

    for x in range(3):
        for y in range(3):
            ball_sprite.rect.x = 472 + x * 85
            ball_sprite.rect.y = 222 + y * 84
            if not (ball_sprite.rect.x == 472 and ball_sprite.rect.y == 306):
                ball_sprite_grup_draw.add(ball_sprite)
                ball_sprite_grup.add(ball_sprite)
                ball_sprite_grup_draw.draw(screen)

    for x in range(1):
        for y in range(3):
            ball_sprite.rect.x = 725 + x * 85
            ball_sprite.rect.y = 222 + y * 83
            ball_sprite_grup_draw.add(ball_sprite)
            ball_sprite_grup.add(ball_sprite)
            ball_sprite_grup_draw.draw(screen)

    for x in range(3):
        for y in range(2):
            ball_sprite.rect.x = 390 + x * 84
            ball_sprite.rect.y = 478 + y * 84
            ball_sprite_grup_draw.add(ball_sprite)
            ball_sprite_grup.add(ball_sprite)
            ball_sprite_grup_draw.draw(screen)


class Board:
    def __init__(self, cell_x, cell_y):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.board = [[0] * cell_x for i in range(cell_y)]
        self.cell_size = 85
        self.top = 30
        self.left = 30

    def draw(self, screen):
        for i in range(self.cell_y):
            for j in range(self.cell_x):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size,
                                  self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    running = True
    cloak = pygame.time.Clock()
    while running:
        cloak.tick(FPS)
        draw_board()
        draw_ball()
        pygame.init()
        screen = pygame.display.set_mode(size)
        running = True
    pygame.display.flip()
    pygame.quit()
