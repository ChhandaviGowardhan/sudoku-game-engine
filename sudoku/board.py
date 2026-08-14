class SudokuBoard:
    def __init__(self, size, grid=None):
        self.size = size
        box_dimensions = {
            4: (2, 2),
            6: (2, 3),
            9: (3, 3)}
        if size not in box_dimensions:
            raise ValueError("Unsupported Sudoku size.")
        self.box_rows, self.box_cols = box_dimensions[size]
        if grid is None:
            self.grid = [
                [0 for _ in range(size)]
                for _ in range(size)]
        else:
            self.grid = grid
    def display(self):
        for row in self.grid:
            print(" ".join(str(value) for value in row))
    def is_empty(self, row, col):
        return self.grid[row][col] == 0
    def find_empty(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.is_empty(row, col):
                    return row, col
        return None
    def is_valid(self, row, col, number):
        # Check row
        if number in self.grid[row]:
            return False
        # Check column
        for r in range(self.size):
            if self.grid[r][col] == number:
                return False
        # Check box
        box_start_row = (row // self.box_rows) * self.box_rows
        box_start_col = (col // self.box_cols) * self.box_cols
        for r in range(box_start_row, box_start_row + self.box_rows):
            for c in range(box_start_col, box_start_col + self.box_cols):
                if self.grid[r][c] == number:
                    return False
        return True
    def validate_grid(self):
        # Check number of rows
        if len(self.grid) != self.size:
            return False
        # Check each row
        for row in self.grid:
            if len(row) != self.size:
                return False
            # Check values
            for value in row:
                if value < 0 or value > self.size:
                    return False
        # Check rows
        for row in range(self.size):
            values = [
                value
                for value in self.grid[row]
                if value != 0]
            if len(values) != len(set(values)):
                return False
        # Check columns
        for col in range(self.size):
            values = [
                self.grid[row][col]
                for row in range(self.size)
                if self.grid[row][col] != 0]
            if len(values) != len(set(values)):
                return False
        # Check boxes
        for box_row in range(0, self.size, self.box_rows):
            for box_col in range(0, self.size, self.box_cols):
                values = []
                for row in range(
                    box_row,
                    box_row + self.box_rows):
                    for col in range(
                        box_col,
                        box_col + self.box_cols):
                        value = self.grid[row][col]
                        if value != 0:
                            values.append(value)
                if len(values) != len(set(values)):
                    return False
        return True
if __name__ == "__main__":
    valid_grid = [
        [1, 0, 0, 4],
        [0, 4, 1, 0],
        [2, 0, 4, 0],
        [4, 3, 0, 1]]
    board = SudokuBoard(4, valid_grid)
    print("Valid grid:", board.validate_grid())