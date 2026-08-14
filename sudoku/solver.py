from .board import SudokuBoard

def solve(board):
    empty_cell = board.find_empty()
    if empty_cell is None:
        return True
    row, col = empty_cell
    for number in range(1, board.size + 1):
        if board.is_valid(row, col, number):
            # Make a choice
            board.grid[row][col] = number
            # Recursively solve the rest
            if solve(board):
                return True
            # Choice didn't work, so undo it
            board.grid[row][col] = 0
    return False

def count_solutions(board, limit=2):
    empty_cell = board.find_empty()
    if empty_cell is None:
        return 1
    row, col = empty_cell
    count = 0
    for number in range(1, board.size + 1):
        if board.is_valid(row, col, number):
            board.grid[row][col] = number
            count += count_solutions(board, limit)
            board.grid[row][col] = 0
            if count >= limit:
                return count
    return count

# if __name__ == "__main__":
#     grid = [
#         [5, 3, 0, 0, 7, 0, 0, 0, 0],
#         [6, 0, 0, 1, 9, 5, 0, 0, 0],
#         [0, 9, 8, 0, 0, 0, 0, 6, 0],
#         [8, 0, 0, 0, 6, 0, 0, 0, 3],
#         [4, 0, 0, 8, 0, 3, 0, 0, 1],
#         [7, 0, 0, 0, 2, 0, 0, 0, 6],
#         [0, 6, 0, 0, 0, 0, 2, 8, 0],
#         [0, 0, 0, 4, 1, 9, 0, 0, 5],
#         [0, 0, 0, 0, 8, 0, 0, 7, 9]
#     ]
#     board = SudokuBoard(9, grid)
#     print("Original Sudoku:")
#     board.display()
#     print("\nSolving...")
#     if solve(board):
#         print("\nSolved Sudoku:")
#         board.display()
#     else:
#         print("\nNo solution exists.")

if __name__ == "__main__":
    grid = [
    [1, 0, 0, 4],
    [0, 4, 1, 0],
    [2, 0, 4, 0],
    [4, 3, 0, 1]
    ]
    board = SudokuBoard(4, grid)
    print("Number of solutions:", count_solutions(board))