import pygame

FPS = 30
CIRCLGROW = pygame.USEREVENT + 1


class Board:
    def __init__(self, cell_x, cell_y):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.board = [[0] * cell_x for i in range(cell_y)]
        self.cell_size = 30
        self.top = 15
        self.left = 15

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for i in range(self.cell_y):
            for j in range(self.cell_x):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                  self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, pygame.Color('black'),
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
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    running = True
    screen.fill(pygame.Color('black'))
    board = Board(5, 6)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
        board.draw(screen)
        pygame.display.flip()
    pygame.quit()
