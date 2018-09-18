import random

def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    g_values = [values[i * n: i * n + n] for i in range(n)]
    return g_values


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    n = pos[1]
    col = [values[i][n] for i in range(len(values))]
    return col


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos"""
    x = pos[0] - pos[0] % 3
    y = pos[1] - pos[1] % 3
    block = []
    for i in range(x, x + 3):
        for j in range(y, y + 3):
            block.append(values[i][j])
    return block


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)

    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                return i, j
    return -1, -1


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции """
    values = set()
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    for i in range(1, 10):
        if not (str(i) in row or str(i) in col or str(i) in block):
            values.add(i)
    return values


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    """
    pos = find_empty_positions(grid)
    if pos == (-1, -1):
        return grid
    possible_values = find_possible_values(grid, pos)
    if possible_values:
        for i in possible_values:
            x = grid[pos[0]][:pos[1]] + [str(i)] + grid[pos[0]][pos[1] + 1:]
            solution = solve(grid[:pos[0]] + [x] + grid[pos[0] + 1:])
            if solution:
                return solution


def check_solution(grid):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(len(grid)):
        row = set(grid[i])
        col = set(get_col(grid, (0, i)))
        if len(row) != 9 or len(col) != 9:
            return False
    for i in [(1, 1), (1, 4), (1, 7), (4, 1), (4, 4), (4, 7), (7, 1), (7, 4), (7, 7)]:
        if len(set(get_block(grid, i))) != 9:
            return False
    return True


def random_pos(N):

    list_pos = []
    while len(list_pos) != N:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        pos = x, y
        if pos not in list_pos:
            list_pos.append(pos)
    return list_pos


def generate_sudoku(N):
    gen_grid = [['.'] * 9 for _ in range(9)]
    fullgrid = solve(gen_grid)

    for x,y in random_pos(N):
        gen_grid[x][y] = fullgrid[x][y]
    return gen_grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)

        if check_solution(solution):
            print('Solution is correct')
        else:
            print('Not today')
