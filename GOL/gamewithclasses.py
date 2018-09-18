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

    def draw_cell_list(self, clist):
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for r in range(self.cell_height):
            for c in range(self.cell_width):
                if clist[r][c].state:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        grid = CellList(self.cell_height, self.cell_width, True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(grid.clist)
            CellList.update(grid)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


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
            self.clist = [[Cell(r,c,random.randint(0,1)) for c in range(ncols)] for r in range(nrows)]
        else:
            self.clist = [[Cell(r, c) for c in range(ncols)] for r in range(nrows)]

    def get_neighbours(self, cell):
        neighbours = []
        row, col = cell.row, cell.col
        positions = [[-1, 1], [-1, 0], [-1, -1], [0, 1], [1, -1], [1, 0], [1, 1], [0, -1]]
        for i in positions:
            if 0 <= row + i[0] < self.nrows \
             and 0 <= col + i[1] < self.ncols:
                neighbours.append(self.clist[row + i[0]][col + i[1]])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.clist)
        for row in range(self.nrows):
            for col in range(self.ncols):
                cell = self.clist[row][col]
                neighbours = self.get_neighbours(cell)
                amt = sum(i.is_alive() for i in neighbours)
                if cell.is_alive():
                    if 1 < amt < 4:
                        new_clist[cell.row][cell.col].state = 1
                    else:
                        new_clist[cell.row][cell.col].state = 0
                else:
                    if amt == 3:
                        new_clist[cell.row][cell.col].state = 1
        self.clist = new_clist
        return self

    def __iter__(self):
        self.numrow = 0
        self.numcol = -1
        return self

    def __next__(self):
        self.n = self.start
        if self.n <= self.end:
            raise StopIteration
        self.n -= self.step
        return self.n

    def __str__(self):
        string = '['
        for row in range(self.nrows):
            if row:
                string += ' ['
            else:
                string += '['
            for col in range(self.ncols):
                string += str(int(self.clist[row][col].state))
                if col != self.ncols - 1:
                    string += ', '
            if row != self.nrows - 1:
                string += '],\n'
            else:
                string += ']'
        string += ']'
        return string

    @classmethod
    def from_file(cls, fname):
        grid = []
        with open(fname) as f:
            for nrow, line in enumerate(f):
                row = []
                for ncol, state in enumerate(line):
                    if state in "01":
                        row.append(Cell(nrow, ncol, int(state)))
                grid.append(row)
            return grid


if __name__ == '__main__':
    game = GameOfLife()
    game.run()
