import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.clist = CellList(self.cell_height, self.cell_width, True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_cell_list()
            self.clist.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self):
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = int(j * self.cell_size) + 1
                y = int(i * self.cell_size) + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.clist.grid[i][j].is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))


class Cell:

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize
        if randomize:
            self.grid = [[Cell(r, c, random.randint(0, 1)) for c in range(ncols)] for r in range(nrows)]
        else:
            self.grid = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]

    def get_neighbours(self, cell):
        neighbours = []
        x = cell.row
        y = cell.col
        neighbours_pos = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y),
                          (x + 1, y + 1), (x, y - 1), (x, y + 1)]
        for i in neighbours_pos:
            if 0 <= i[0] <= self.nrows - 1 and 0 <= i[1] <= self.ncols - 1:
                neighbours.append(self.grid[i[0]][i[1]])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.grid)
        for row in range(self.nrows):
            for col in range(self.ncols):
                cell = self.grid[row][col]
                neighbours = self.get_neighbours(cell)
                n = sum(i.is_alive() for i in neighbours)
                if n == 3:
                    new_clist[cell.row][cell.col].state = 1
                elif n == 2 and cell.is_alive():
                    new_clist[cell.row][cell.col].state = 1
                else:
                    new_clist[cell.row][cell.col].state = 0
        self.grid = new_clist
        return self

    def __iter__(self):
        self.r = 0
        self.c = 0
        return self

    def __next__(self):
        if self.r == self.nrows:
            raise StopIteration
        g = self.grid[self.r][self.c]
        self.c += 1
        if self.c == self.ncols:
            self.c = 0
            self.r += 1
        return g

    def __str__(self):
        string = '['
        for row in range(self.nrows):
            if row:
                string += ' ['
            else:
                string += '['
            for col in range(self.ncols):
                string += str(int(self.grid[row][col].state))
                if col != self.ncols - 1:
                    string += ', '
            if row != self.nrows - 1:
                string += '],\n'
            else:
                string += ']'
        string += ']'
        return string

    @classmethod
    def from_file(cls, filename):
        fgrid = []
        with open(filename) as f:
            for nrow, line in enumerate(f):
                row = [Cell(nrow, ncol, int(state)) for ncol, state in enumerate(line) if state in "01"]
                fgrid.append(row)
        clist = cls(len(fgrid), len(fgrid[0]))
        clist.grid = fgrid
        return clist


if __name__ == '__main__':
    game = GameOfLife()
    game.run()

