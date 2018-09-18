import pygame
from pygame.locals import *
import random


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

        # Создание списка клеток
        self.cell_list()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()

            # Отрисовка списка клеток
            self.draw_cell_list(self.clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.clist = self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        if randomize is True:
            for i in range(self.cell_height):
                c = list()
                for j in range(self.cell_width):
                    x = random.randint(0, 1)
                    c.append(x)
                self.clist.append(c)
        else:
            self.clist = [[0] * self.cell_width for _ in range(self.cell_height)]
        return self.clist

    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if clist[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        x, y = cell
        neighbours_pos = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y),
                          (x + 1, y + 1), (x, y - 1), (x, y + 1)]
        for i in neighbours_pos:
            if 0 <= i[0] <= self.cell_height - 1 and 0 <= i[1] <= self.cell_width - 1:
                neighbours.append(self.clist[i[0]][i[1]])
        return neighbours

    def update_cell_list(self, clist):
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param clist: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = [[0] * self.cell_width for _ in range(self.cell_height)]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                n = self.get_neighbours((i, j)).count(1)
                if clist[i][j] and 1 < n < 4:
                    new_clist[i][j] = 1
                elif clist[i][j] == 0 and n == 3:
                    new_clist[i][j] = 1
                else:
                    new_clist[i][j] = 0
        clist = new_clist
        return clist


game = GameOfLife()
game.run()
