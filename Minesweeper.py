import numpy
import random


def get_adjacent_cells(i, j, m, n):
    adjacent_cells = []
    if i > 0:
        adjacent_cells.append((i-1, j))
    if i > 0 and j+1 < n:
        adjacent_cells.append((i-1, j+1))
    if i > 0 and j > 0:
        adjacent_cells.append((i-1, j-1))
    if i+1 < m:
        adjacent_cells.append((i+1, j))
    if i+1 < m and j+1 < n:
        adjacent_cells.append((i+1, j+1))
    if i+1 < m and j > 0:
        adjacent_cells.append((i+1, j-1))
    if j > 0:
        adjacent_cells.append((i, j-1))
    if j+1 < n:
        adjacent_cells.append((i, j+1))
    return adjacent_cells


def sum_adjacent_mines(field, adjacent_cells):
    sum = 0
    for cell in adjacent_cells:
        value = field[cell[0]][cell[1]]
        if value == -1:
            sum += 1
    return sum


def create_field(rows, columns, mines):
    field = numpy.zeros((rows, columns), int)
    while mines > 0:
        i = random.randint(0, rows - 1)
        j = random.randint(0, columns - 1)
        if field[i][j] == 0:
            field[i][j] = -1
            mines -= 1
    for i in range(rows):
        for j in range(columns):
            if field[i][j] == 0:
                field[i][j] = sum_adjacent_mines(field, get_adjacent_cells(i, j, rows, columns))
    return field
