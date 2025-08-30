import random
import os
import time

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
PURPLE = "\033[35m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

difficulty_levels = {
    1: (5, 5, 5),
    2: (10, 10, 10),
    3: (15, 15, 25)
}

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),         (0, 1),
    (1, -1), (1, 0), (1, 1)
]

def initialize_board(rows, cols, mines, first_x, first_y):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    revealed = [[0 for _ in range(cols)] for _ in range(rows)]

    mine_positions = set()
    while len(mine_positions) < mines:
        x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if (x, y) == (first_x, first_y) or (x, y) in mine_positions:
            continue
        mine_positions.add((x, y))
        grid[x][y] = -1
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != -1:
                grid[nx][ny] += 1

    return grid, revealed

def print_board(grid, revealed, ai_suggestion):
    clear_screen()
    print("\n  ", end="")
    for j in range(len(grid[0])):
        print(f"  {j:2} ", end="  ")
    print("\n")

    for i in range(len(grid)):
        print("   +" + "------+" * len(grid[0]))
        for part in range(2):
            print(f"{i:2} |" if part == 0 else "   |", end="")
            for j in range(len(grid[0])):
                if ai_suggestion == (i, j):
                    print(f"{PURPLE}  ??  {RESET}|", end="")
                elif revealed[i][j] == 1:
                    if grid[i][j] == -1:
                        print(f"{RED}  **  {RESET}|", end="")
                    elif grid[i][j] == 0:
                        print("      |", end="")
                    else:
                        print(f"   {YELLOW}{grid[i][j]}  {RESET}|", end="")
                elif revealed[i][j] == 2:
                    print(f"{GREEN}  FF  {RESET}|", end="")
                else:
                    print(f"{BLUE}  ##  {RESET}|", end="")
            print("")
    print("   +" + "------+" * len(grid[0]))

def reveal_cell(grid, revealed, x, y):
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or revealed[x][y] != 0:
        return
    revealed[x][y] = 1
    if grid[x][y] == 0:
        for dx, dy in directions:
            reveal_cell(grid, revealed, x + dx, y + dy)

def check_win(grid, revealed):
    return all(revealed[i][j] or grid[i][j] == -1 for i in range(len(grid)) for j in range(len(grid[0])))

def ai_suggest_move(grid, revealed):
    safe_moves = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if revealed[i][j] == 0]
    return random.choice(safe_moves) if safe_moves else None

def main():
    rows, cols, mines = difficulty_levels[2]
    grid, revealed = initialize_board(rows, cols, mines, rows // 2, cols // 2)
    game_over, win = False, False

    while not game_over:
        ai_suggestion = ai_suggest_move(grid, revealed)
        print_board(grid, revealed, ai_suggestion)

        try:
            action, x, y = input("Enter move (r x y to reveal, f x y to flag): ").split()
            x, y = int(x), int(y)
        except ValueError:
            print("Invalid input. Try again.")
            continue

        if action == 'r':
            if grid[x][y] == -1:
                print("Game Over! You hit a mine.")
                revealed[x][y] = 1
                game_over = True
            else:
                reveal_cell(grid, revealed, x, y)
                if check_win(grid, revealed):
                    print("Congratulations! You win!")
                    game_over = True
                    win = True
        elif action == 'f':
            revealed[x][y] = 2 if revealed[x][y] == 0 else 0
        else:
            print("Invalid move. Try again.")

    print_board(grid, revealed, None)

if __name__ == "__main__":
    main()
