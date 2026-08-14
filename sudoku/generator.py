import random
from .board import SudokuBoard
from .solver import count_solutions

def generate_solution(size):
    board = SudokuBoard(size)
    fill_board(board)
    return board

def fill_board(board):
    empty_cell = board.find_empty()
    if empty_cell is None:
        return True
    row, col = empty_cell
    numbers = list(range(1, board.size + 1))
    random.shuffle(numbers)
    for number in numbers:
        if board.is_valid(row, col, number):
            board.grid[row][col] = number
            if fill_board(board):
                return True
            board.grid[row][col] = 0
    return False

def generate_puzzle(size, removals):
    board = generate_solution(size)
    positions = [
        (row, col)
        for row in range(size)
        for col in range(size)
    ]
    random.shuffle(positions)
    removed = 0
    for row, col in positions:
        if removed >= removals:
            break
        original_value = board.grid[row][col]
        board.grid[row][col] = 0
        solution_count = count_solutions(board)
        if solution_count == 1:
            removed += 1
        else:
            board.grid[row][col] = original_value
    return board

if __name__ == "__main__":
    board = generate_puzzle(4,6)
    print("Generated Sudoku Puzzle:\n")
    board.display()
    print("\nNumber of solutions:",
          count_solutions(board))