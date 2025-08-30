import random

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1), (1, 0), (1, 1)
]

class Minesweeper:
    def __init__(self, rows=10, cols=10, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid, self.revealed = self._initialize_board()
        self.game_over = False
        self.win = False

    def _initialize_board(self):
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        revealed = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        mines_placed = 0
        
        while mines_placed < self.mines:
            x, y = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if grid[x][y] != -1:
                grid[x][y] = -1
                mines_placed += 1
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.cols and grid[nx][ny] != -1:
                        grid[nx][ny] += 1
        
        return grid, revealed

    def reveal_cell(self, x, y):
        if self.game_over or self.revealed[x][y] != 0:
            return "invalid"
        
        self.revealed[x][y] = 1
        
        if self.grid[x][y] == -1:
            self.game_over = True
            return "mine"
        
        if self.grid[x][y] == 0:
            self._reveal_adjacent(x, y)
        
        if self._check_win():
            self.game_over = True
            self.win = True
            return "win"
        
        return "safe"

    def _reveal_adjacent(self, x, y):
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.revealed[nx][ny] == 0:
                self.reveal_cell(nx, ny)

    def flag_cell(self, x, y):
        if self.revealed[x][y] == 0:
            self.revealed[x][y] = 2
        elif self.revealed[x][y] == 2:
            self.revealed[x][y] = 0

    def _check_win(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] != -1 and self.revealed[x][y] != 1:
                    return False
        return True

    def get_state(self):
        return {
            "grid": self.grid,
            "revealed": self.revealed,
            "rows": self.rows,
            "cols": self.cols,
            "game_over": self.game_over,
            "win": self.win
        }