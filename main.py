from time import sleep
import sys
from pathlib import Path

import pygame as p
from random import randrange
from pygame.locals import *


class GameOfLife:
    def __init__(self, window_size_x: int = 1000, window_size_y: int = 500, cell_size=10):
        self.window_size_x = window_size_x - window_size_x % cell_size
        self.window_size_y = window_size_y - window_size_y % cell_size
        self.field_size_x = window_size_x // cell_size
        self.field_size_y = window_size_y // cell_size

        # Константы цветов RGB
        self.BLACK = (0, 0, 0)
        self.CELL = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        # Создаем окно
        self.root = p.display.set_mode((self.window_size_x, self.window_size_y))
        # 2х мерный список с помощью генераторных выражений
        self.cells = [[0 for y in range(self.field_size_y)] for x in range(self.field_size_x)]
        self.cells_2 = [[0 for y in range(self.field_size_y)] for x in range(self.field_size_x)]

        self.cell_size = cell_size

    def insert_figure(self, figure_file: str, x_left: int=None, y_top: int=None) -> None:
        figure = self.figure_from_file(figure_file)
        x_field_size = len(self.cells[0])
        y_field_size = len(self.cells)
        x_figure_size = len(figure[0])
        y_figure_size = len(figure)

        if x_left is None:
            x_left = (self.field_size_x // 2) - (x_figure_size // 2)
        if y_top is None:
            y_top = (self.field_size_y // 2) - (y_figure_size // 2)

        if x_figure_size + x_left > x_field_size or y_figure_size + y_top > y_field_size:
            print("figure size is out of bounds of field")
        elif x_left < 0 or y_top < 0:
            print("invalid insert point")
        for index_y, y in enumerate(figure):
            for index_x, x in enumerate(y):
                self.cells[(index_y + y_top) % self.field_size_y][(index_x + x_left) % self.field_size_x] = x

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
                        p.draw.rect(self.root, self.CELL, p.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))

            for y in range(len(self.cells)):
                for x in range(len(self.cells[y])):
                    self.cells_2[y][x] = self.is_live(x, y)
            for y in range(len(self.cells)):
                for x in range(len(self.cells[y])):
                    self.cells[y][x] = self.cells_2[y][x]

            # Рисуем сетку
            for i in range(0, self.root.get_height() // self.cell_size):
                p.draw.line(self.root, (200, 200, 200), (0, i * self.cell_size), (self.root.get_width(), i * self.cell_size))
            for j in range(0, self.root.get_width() // self.cell_size):
                p.draw.line(self.root, (200, 200, 200), (j * self.cell_size, 0), (j * self.cell_size, self.root.get_height()))

            p.display.update()
            sleep(.1)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        figure_file = Path(sys.argv[1])
        if figure_file.is_file():
            a = GameOfLife(1000, 1000, 10)
            a.insert_figure('{}'.format(sys.argv[1]))
            a.process()
        else:
            print('Error: figure file does not exists')
    else:
        print('Error: wrong usage. Please select figure file as second argument')
        print('Example: python3 {} figures/blinker_ship'.format(sys.argv[0]))
