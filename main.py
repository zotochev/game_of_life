# Импорты
from time import sleep

import pygame as p
from random import randrange
from pygame.locals import *


class GameOfLife:

    def __init__(self, window_size_x: int = 1000, window_size_y: int = 1000):
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y

        # Константы цветов RGB
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        # Создаем окно
        self.root = p.display.set_mode((self.window_size_x, self.window_size_y))
        # 2х мерный список с помощью генераторных выражений
        # cells = [[randrange(2) for y in range(100)] for x in range(100)]
        self.cells = [[0 for y in range(100)] for x in range(100)]
        self.cells_2 = [[0 for y in range(100)] for x in range(100)]

    def insert_figure(self, figure_file: str, x_left: int, y_top: int) -> None:
        figure = self.figure_from_file(figure_file)
        x_field_size = len(self.cells[0])
        y_field_size = len(self.cells)
        x_figure_size = len(figure[0])
        y_figure_size = len(figure)

        if x_figure_size + x_left > x_field_size or y_figure_size + y_top > y_field_size:
            print("figure size is out of bounds of field")
        elif x_left < 0 or y_top < 0:
            print("invalid insert point")
        for index_y, y in enumerate(figure):
            for index_x, x in enumerate(y):
                self.cells[index_y + y_top][index_x + x_left] = x

    @staticmethod
    def figure_from_file(file: str) -> list:
        """
        http://www.radicaleye.com/lifepage/picgloss/picgloss.html
        """
        result = list()

        with open(file) as f:
            for row in f:
                result.append(list(map(lambda x: 1 if x == '*' else 0, list(row.strip()))))
        return result

    @staticmethod
    def new_coord(coord, size):
        if coord == 0:
            return size - 1, coord, coord + 1
        elif coord == size - 1:
            return coord - 1, coord, 0
        else:
            return coord - 1, coord, coord + 1

    def sum_near(self, cell_array: list, x, y):
        x_size = len(cell_array[0])
        y_size = len(cell_array)

        new_x = self.new_coord(x, x_size)
        new_y = self.new_coord(y, y_size)

        return cell_array[new_y[0]][new_x[0]] \
            + cell_array[new_y[0]][new_x[1]]  \
            + cell_array[new_y[0]][new_x[2]]  \
            + cell_array[new_y[2]][new_x[0]]  \
            + cell_array[new_y[2]][new_x[1]]  \
            + cell_array[new_y[2]][new_x[2]]  \
            + cell_array[new_y[1]][new_x[0]]  \
            + cell_array[new_y[1]][new_x[2]]

    def is_live(self, x, y):
        if self.cells[y][x] == 1:
            if self.sum_near(self.cells, x, y) in (2, 3):
                return 1
            else:
                return 0
        else:
            if self.sum_near(self.cells, x, y) in (3, ):
                return 1
            else:
                return 0

    def process(self):
        # Основной цикл
        while True:
            # Заполняем экран белым цветом
            self.root.fill(self.WHITE)

           # Нужно чтобы виндовс не думал что программа "не отвечает"
            for i in p.event.get():
                if i.type == QUIT:
                    quit()

            # Проходимся по всем клеткам
            for y in range(len(self.cells)):
                for x in range(len(self.cells[y])):
                    if self.cells[y][x]:
                        p.draw.rect(self.root, (0, 0, 0), p.Rect(y * 10, x * 10, 10, 10))
                    else:
                        p.draw.rect(self.root, (255, 255, 255), p.Rect(y * 10, x * 10, 10, 10))

            for y in range(len(self.cells)):
                for x in range(len(self.cells[y])):
                    self.cells_2[y][x] = self.is_live(x, y)
            for y in range(len(self.cells)):
                for x in range(len(self.cells[y])):
                    self.cells[y][x] = self.cells_2[y][x]

            # Рисуем сетку
            for i in range(0, self.root.get_height() // 10):
                p.draw.line(self.root, (200, 200, 200), (0, i * 10), (self.root.get_width(), i * 10))
            for j in range(0, self.root.get_width() // 10):
                p.draw.line(self.root, (200, 200, 200), (j * 10, 0), (j * 10, self.root.get_height()))

            p.display.update()
            sleep(0.1)


if __name__ == '__main__':
    a = GameOfLife(1000, 1000)
    a.insert_figure('figures/blinker_ship', 50, 50)
    a.process()
