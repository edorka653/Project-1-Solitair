import pygame
import os
import sys


class Board:
    def __init__(self, cell_x, cell_y):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.board = [[0] * cell_x for i in range(cell_y)]
        self.cell_size = 85
        self.top = 40
        self.left = 201

    def draw(self, screen):
        for i in range(self.cell_y):
            for j in range(self.cell_x):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                  self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                  self.cell_size))

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        if 0 <= cell_x <= self.cell_x and 0 <= cell_y <= self.cell_y:
            return cell_x, cell_y
        else:
            return None

    def on_click(self, cell):
        if cell:
            for i in range(self.cell_x):
                self.board[cell[1]][i] = (self.board[cell[1]][i] + 1) % 2
            for i in range(self.cell_y):
                self.board[i][cell[0]] = (self.board[i][cell[0]] + 1) % 2
            self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2
            print(cell)


if __name__ == '__main__':
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

    pygame.init()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    running = True
    cloak = pygame.time.Clock()
    FPS = 30
    ball_sprite_grup = pygame.sprite.Group()
    Br = Board(7, 7)

    while running:
        draw_board()
        draw_ball()
        Br.draw(screen)
        pygame.display.flip()
        cloak.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Br.get_click(event.pos)

    pygame.quit()
