import pygame
import os
import sys

all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
FPS = 30


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("Board.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Setka:
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
                if self.board[j][i] == 0:
                    pygame.draw.rect(screen, pygame.Color('white'),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size,
                                      self.cell_size), 1)

                else:
                    pygame.draw.rect(screen, pygame.Color('green'),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size,
                                      self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click_left(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click_left(cell)
        return cell

    def get_click_right(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click_right(cell)
        return cell

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        if 0 <= cell_x <= self.cell_x and 0 <= cell_y <= self.cell_y and \
                not ((cell_y < 2 or cell_y > 4) and (cell_x < 2 or cell_x > 4)):
            return cell_x, cell_y
        else:
            return None

    def on_click_left(self, cell):
        if cell:
            for i in range(7):
                for j in range(7):
                    self.board[i][j] = 0
            self.board[cell[0]][cell[1]] = (self.board[cell[0]][cell[1]] + 1) % 2
            return cell

    def on_click_right(self, cell):
        main_pos = 0
        for i in range(7):
            for j in range(7):
                if self.board[i][j]:
                    main_pos = i, j
        global ball
        if cell and main_pos:
            if cell[0] == (main_pos[0] + 2) and cell[1] == main_pos[1]:
                if ball[cell[1]][cell[0]] and ball[cell[1]][cell[0] - 1] and \
                        not (ball[cell[1]][cell[0] - 2]):
                    ball[cell[1]][cell[0]].rect = ball[cell[1]][cell[0]].rect.move(-170, 0)
                    ball[cell[1]][cell[0]], ball[cell[1]][cell[0] - 2] = \
                        ball[cell[1]][cell[0] - 2], ball[cell[1]][cell[0]]
            elif cell[0] == (main_pos[0] - 2) and cell[1] == main_pos[1]:
                if ball[cell[1]][cell[0]] and ball[cell[1]][cell[0] + 1] and \
                        not (ball[cell[1]][cell[0] + 2]):
                    ball[cell[1]][cell[0]].rect = ball[cell[1]][cell[0]].rect.move(170, 0)
                    ball[cell[1]][cell[0]], ball[cell[1]][cell[0] + 2] = \
                        ball[cell[1]][cell[0] + 2], ball[cell[1]][cell[0]]
            elif cell[1] == (main_pos[1] + 2) and cell[0] == main_pos[0]:
                if ball[cell[0]][cell[1]] and ball[cell[0]][cell[1] - 1] and \
                        not (ball[cell[0]][cell[1] - 2]):
                    ball[cell[1]][cell[0]].rect = ball[cell[1]][cell[0]].rect.move(0, -170)
                    ball[cell[0]][cell[1]], ball[cell[0]][cell[1] - 2] = \
                        ball[cell[0]][cell[1] - 2], ball[cell[0]][cell[1]]
            elif cell[1] == (main_pos[1] - 2) and cell[0] == main_pos[0]:
                if ball[cell[0]][cell[1]] and ball[cell[0]][cell[1] + 1] and \
                        not (ball[cell[0]][cell[1] + 2]):
                    ball[cell[1]][cell[0]].rect = ball[cell[1]][cell[0]].rect.move(0, 170)
                    ball[cell[0]][cell[1]], ball[cell[0]][cell[1] + 2] = \
                        ball[cell[0]][cell[1] + 2], ball[cell[0]][cell[1]]
            else:
                return


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("Ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, event_pos, type):
        if type == 3:
            pos_move = Sr.get_click_right(event_pos)
            if pos_move is None:
                return
            if not ((pos_move[0] < 2 or pos_move[0] > 4) and
                    (pos_move[1] < 2 or pos_move[1] > 4)):
                return
            Sr.board[pos_move[0]][pos_move[1]] = 1
            my_pos = (self.rect.left, self.rect.top)
            if pos_move[0] != my_pos[0] or pos_move[1] == my_pos[1]:
                print('Можно сделать ход')
            elif pos_move[0] == my_pos[0] or pos_move[1] != my_pos[1]:
                print('Можно сделать ход')
        if type == 1:
            pos_move = Sr.get_click_left(event_pos)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Ancent Franch Solitai', "",
                  "Правила игры:",
                  "RMB - Выбрать шарик который хотите передвинуть",
                  "LMB - Выбрать место, куда хотите сдвинуть шарик",
                  "Цель игры - убрать все шарики с доски"
                  ]

    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    running = True
    start_screen()
    Board(1, 1, all_sprites)
    ball = [[0] * 7 for i in range(7)]
    for x in range(2, 5):
        for y in range(2):
            ball[y][x] = Ball(388 + (x - 2) * 84, 53 + y * 84, all_sprites)

    for x in range(3):
        for y in range(2, 5):
            ball[y][x] = Ball(217 + x * 85, 223 + (y - 2) * 84, all_sprites)
    for x in range(3, 6):
        for y in range(2, 5):
            X = 472 + (x - 3) * 85
            Y = 222 + (y - 2) * 84
            if not (X == 472 and Y == 306):
                ball[y][x] = Ball(472 + (x - 3) * 85, 222 + (y - 2) * 84, all_sprites)
    for x in range(6, 7):
        for y in range(2, 5):
            ball[y][x] = Ball(725 + (x - 6) * 85, 222 + (y - 2) * 83, all_sprites)

    for x in range(2, 5):
        for y in range(5, 7):
            ball[y][x] = Ball(390 + (x - 2) * 84, 478 + (y - 5) * 84, all_sprites)
    all_sprites.draw(screen)
    Sr = Setka(7, 7)
    while running:
        pygame.display.flip()
        clock.tick(FPS)
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Sr.get_click_left(event.pos)
                if event.button == 3:
                    all_sprites.update(event.pos, 3)
        all_sprites.draw(screen)
        Sr.draw(screen)
    pygame.quit()
