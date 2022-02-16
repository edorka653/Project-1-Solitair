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
        self.board = [[1] * cell_x for i in range(cell_y)]
        self.put_balls()
        self.cell_size = 85
        self.top = 40
        self.left = 201
        self.active_cell = None
        self.empty_cell = load_image('Empty_Ball.png')

    def init_draw(self):
        image = pygame.Surface([self.cell_size * self.cell_x, self.cell_size * self.cell_y])
        image = image.convert()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        return image

    def put_balls(self):
        for x in range(2, 5):
            for y in range(2):
                self.board[y][x] = Ball(388 + (x - 2) * 84, 53 + y * 84, all_sprites)

        for x in range(3):
            for y in range(2, 5):
                self.board[y][x] = Ball(217 + x * 85, 223 + (y - 2) * 84, all_sprites)
        for x in range(3, 6):
            for y in range(2, 5):
                X = 472 + (x - 3) * 85
                Y = 222 + (y - 2) * 84
                if not (X == 472 and Y == 306):
                    self.board[y][x] = Ball(472 + (x - 3) * 85, 222 + (y - 2) * 84, all_sprites)
                else:
                    self.board[y][x] = 0
        for x in range(6, 7):
            for y in range(2, 5):
                self.board[y][x] = Ball(725 + (x - 6) * 85, 222 + (y - 2) * 83, all_sprites)

        for x in range(2, 5):
            for y in range(5, 7):
                self.board[y][x] = Ball(390 + (x - 2) * 84, 478 + (y - 5) * 84, all_sprites)

    def get_click_left(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click_left(cell)

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
        self.active_cell = cell
        self.draw_frame(cell)

    def draw_frame(self, cell):
        image = pygame.Surface([self.cell_size * self.cell_x, self.cell_size * self.cell_y])
        image = image.convert()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        pygame.draw.rect(image, pygame.Color((255, 255, 255, 0)),
                         (cell[0] * self.cell_size, cell[1] * self.cell_size, self.cell_size,
                          self.cell_size), 1)
        self.image = image

    def check_end(self):
        for i in range(7):
            for j in range(7):
                if type(self.board[i][j]) != int:
                    for u, v in (-1, 0), (1, 0), (0, -1), (0, 1):
                        if 0 <= i + u * 2 < 7 and 0 <= j + v * 2 < 7:
                            if 2 <= i + u * 2 < 5 or 2 <= j + v * 2 < 5:
                                if self.board[i + u][j + v]:
                                    if self.board[i + u * 2][j + v * 2] == 0:
                                        return True
        return False

    def on_click_right(self, cell):
        empty_cell = self.active_cell
        if cell and empty_cell:
            if cell[0] == (empty_cell[0] + 2) and cell[1] == empty_cell[1]:
                if cell[0] - 2 >= 0 and self.board[cell[1]][cell[0]] and self.board[cell[1]][cell[0] - 1] and \
                        not (self.board[cell[1]][cell[0] - 2]):
                    self.board[cell[1]][cell[0]].rect = self.board[cell[1]][cell[0]].rect.move(-170, 0)
                    self.board[cell[1]][cell[0]], self.board[cell[1]][cell[0] - 2] = \
                        self.board[cell[1]][cell[0] - 2], self.board[cell[1]][cell[0]]
                    self.board[cell[1]][cell[0] - 1].image = self.empty_cell
                    self.board[cell[1]][cell[0] - 1] = 0


            elif cell[0] == (empty_cell[0] - 2) and cell[1] == empty_cell[1]:
                if cell[0] + 2 < 7 and self.board[cell[1]][cell[0]] and self.board[cell[1]][cell[0] + 1] and \
                        not (self.board[cell[1]][cell[0] + 2]):
                    self.board[cell[1]][cell[0]].rect = self.board[cell[1]][cell[0]].rect.move(170, 0)
                    self.board[cell[1]][cell[0]], self.board[cell[1]][cell[0] + 2] = \
                        self.board[cell[1]][cell[0] + 2], self.board[cell[1]][cell[0]]
                    self.board[cell[1]][cell[0] + 1].image = self.empty_cell
                    self.board[cell[1]][cell[0] + 1] = 0

            elif cell[1] == (empty_cell[1] + 2) and cell[0] == empty_cell[0]:
                if cell[1] - 2 >= 0 and self.board[cell[1]][cell[0]] and self.board[cell[1] - 1][cell[0]] and \
                        not (self.board[cell[1] - 2][cell[0]]):
                    self.board[cell[1]][cell[0]].rect = self.board[cell[1]][cell[0]].rect.move(0, -170)
                    self.board[cell[1]][cell[0]], self.board[cell[1] - 2][cell[0]] = \
                        self.board[cell[1] - 2][cell[0]], self.board[cell[1]][cell[0]]
                    self.board[cell[1] - 1][cell[0]].image = self.empty_cell
                    self.board[cell[1] - 1][cell[0]] = 0

            elif cell[1] == (empty_cell[1] - 2) and cell[0] == empty_cell[0]:
                if cell[1] + 2 < 7 and self.board[cell[1]][cell[0]] and self.board[cell[1] + 1][cell[0]] and \
                        not (self.board[cell[1] + 2][cell[0]]):
                    self.board[cell[1]][cell[0]].rect = self.board[cell[1]][cell[0]].rect.move(0, 170)
                    self.board[cell[1]][cell[0]], self.board[cell[1] + 2][cell[0]] = \
                        self.board[cell[1] + 2][cell[0]], self.board[cell[1]][cell[0]]
                    self.board[cell[1] + 1][cell[0]].image = self.empty_cell
                    self.board[cell[1] + 1][cell[0]] = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = load_image("Ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, event_pos, type):
        if type == 3:
            Sr.get_click_right(event_pos)
        if type == 1:
            Sr.get_click_left(event_pos)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['French Solitair', "",
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


def end_screen():
    score = 0
    for i in range(7):
        for j in range(7):
            if type(Sr.board[i][j]) != int:
                score += 1
    score = 32 - score
    intro_text = [f'Игра окончена']
    if score < 31:
        intro_text.extend(['Но вы можете ЛУЧШЕ!', f'Ваш счёт: {score}'])
    else:
        intro_text.append('Вы ПОБЕДИЛИ!')

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
    bg = load_image('BackGround.png')
    pygame.init()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    running = True
    start_screen()
    screen.blit(bg, (0, 0))
    Board(1, 1, all_sprites)
    all_sprites.draw(screen)
    Sr = Setka(7, 7)
    end_flag = False
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
                    if not(Sr.check_end()):
                        end_flag = True
        all_sprites.draw(screen)
        Sr.init_draw()
        if end_flag:
            screen.fill('Black')
            end_screen()
    pygame.quit()
