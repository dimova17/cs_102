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
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if clist[row][col].state:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (col * self.cell_size,
                                      row * self.cell_size,
                                      self.cell_size,
                                      self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (col * self.cell_size,
                                      row * self.cell_size,
                                      self.cell_size,
                                      self.cell_size))

    def cell_list(self, randomize=True):
        self.clist = CellList(self.cell_width, self.cell_height, randomize)
        self.grid = self.clist.clist

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
            self.cell_list()
            self.clist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row, col, state=0):
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
            self.clist = [[Cell(row, col, random.randint(0, 1))
                           for col in range(ncols)]
                          for row in range(nrows)]
        else:
            self.clist = [[Cell(row, col) for col in range(ncols)]
                          for row in range(nrows)]

    def get_neighbours(self, cell):
        neighbours = []
        row, col = cell.row, cell.col
        positions = [[-1, -1], [-1, 0], [-1, 1], [0, -1],
                     [0, 1], [1, -1], [1, 0], [1, 1]]
        for neighbour in positions:
            if (0 <= neighbour[0] + row < self.nrows) and\
               (0 <= neighbour[1] + col < self.ncols):
                    neighbours.append(self.clist[neighbour[0] + row]
                                                [neighbour[1] + col])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.clist)
        for row in range(self.nrows):
            for col in range(self.ncols):
                cell = self.clist[row][col]
                neighbours = self.get_neighbours(cell)
                amount = sum(neighbour.is_alive() for neighbour in neighbours)
                if cell.is_alive():
                    if (1 < amount < 4):
                        new_clist[cell.row][cell.col].state = 1
                    else:
                        new_clist[cell.row][cell.col].state = 0
                else:
                    if amount == 3:
                        new_clist[cell.row][cell.col].state = 1

        return self

    def __iter__(self):
        self.numrow = 0
        self.numcol = -1
        return self

    def __next__(self):
        self.numcol += 1
        if self.numcol == self.ncols:
            self.numcol = 0
            self.numrow += 1
        if self.numrow == self.nrows:
            raise StopIteration
        return self.clist[self.numrow][self.numcol]

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
    def from_file(cls, filename):
        grid = []
        with open(filename) as f:
            for row, line in enumerate(f):
                grid.append([Cell(row, col, int(state))
                             for col, state in enumerate(line)
                             if state in '01'])
        clist = cls(len(grid), len(grid[0]))
        clist.clist = grid
        return clist

if __name__ == '__main__':
    game = GameOfLife(320, 240, 10)
    game.run()
