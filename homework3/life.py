import pathlib
import random

from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for y in range(self.rows):
                for x in range(self.cols):
                    grid[y][x] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        y, x = cell
        coords = [(x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1),
                  (x - 1, y - 1)]

        # For non-endless pole
        _coords = []
        for x, y in coords:
            if 0 <= x < self.cols and 0 <= y < self.rows:
                _coords.append((x, y))
        coords = _coords

        return [self.curr_generation[y1 % self.rows][x1 % self.cols] for x1, y1 in coords]

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = self.create_grid()
        for y in range(self.rows):
            for x in range(self.cols):
                neighbours_n = self.get_neighbours((y, x)).count(1)
                if self.curr_generation[y][x] == 0:
                    if neighbours_n == 3:
                        new_grid[y][x] = 1
                else:
                    if neighbours_n in [2, 3]:
                        new_grid[y][x] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceed:
            self.prev_generation = self.curr_generation.copy()
            self.curr_generation = self.get_next_generation()
            self.n_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.n_generation >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as file:
            grid = [[int(x) for x in list(row)] for row in file.readlines()]
        rows, cols = len(grid), len(grid[0])

        game = GameOfLife((rows, cols))
        game.curr_generation = grid

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as file:
            for row in self.curr_generation:
                file.write(''.join([str(x) for x in row]))
                file.write('\n')
