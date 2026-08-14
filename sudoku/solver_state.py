import copy
from .board import SudokuBoard

class SolverState:
    def __init__(self, board):
        self.board = board
        self.candidates = {}
        self.techniques_used = {}
        self.refresh_candidates()
    def place_number(self, row, col, number):
        self.board.grid[row][col] = number
        self.refresh_candidates()
    def find_candidate_singles(self):
        singles = []
        for (row, col), candidates in self.candidates.items():
            if len(candidates) == 1:
                number = next(iter(candidates))
                singles.append(
                    (row, col, number)
                )
        return singles
    def eliminate_candidates(self, row, col, numbers):
        if (row, col) not in self.candidates:
            return False
        old_candidates = self.candidates[(row, col)].copy()
        self.candidates[(row, col)] -= numbers
        return (
            self.candidates[(row, col)]
            != old_candidates
        )
    def refresh_candidates(self):
        old_candidates = self.candidates.copy()
        self.candidates = {}
        for row in range(self.board.size):
            for col in range(self.board.size):
                if not self.board.is_empty(row, col):
                    continue
                cell = (row, col)
                valid_candidates = self.get_candidates(row, col)
                if cell in old_candidates:
                # Preserve previous logical eliminations
                # while removing candidates invalidated by
                # newly placed numbers.
                    self.candidates[cell] = (
                        old_candidates[cell] & valid_candidates
                    )
                else:
                # First initialization
                    self.candidates[cell] = valid_candidates
    def get_candidates(self, row, col):
        candidates = set(
            range(1, self.board.size + 1))
        # Remove row values
        for value in self.board.grid[row]:
            candidates.discard(value)
        # Remove column values
        for r in range(self.board.size):
            candidates.discard(
                self.board.grid[r][col])
        # Remove box values
        box_start_row = (
            row // self.board.box_rows
        ) * self.board.box_rows
        box_start_col = (
            col // self.board.box_cols
        ) * self.board.box_cols
        for r in range(
            box_start_row,
            box_start_row + self.board.box_rows):
            for c in range(
                box_start_col,
                box_start_col + self.board.box_cols):
                candidates.discard(
                    self.board.grid[r][c])
        return candidates
    def is_solved(self):
        for row in range(self.board.size):
            for col in range(self.board.size):
                if self.board.is_empty(row, col):
                    return False
        return True
    def record_technique(self, technique):
        if technique not in self.techniques_used:
            self.techniques_used[technique] = 0
        self.techniques_used[technique] += 1
    

if __name__ == "__main__":
    grid = [
    [1, 0, 0, 4],
    [0, 4, 1, 0],
    [2, 0, 4, 0],
    [4, 3, 0, 1]
]
    board = SudokuBoard(4, copy.deepcopy(grid))
    state = SolverState(board)
    print("Before:")
    for cell, values in state.candidates.items():
        print(cell, "→", values)
    print("\nPlacing 2 at (0, 1)...")
    state.place_number(0, 1, 2)
    print("\nAfter:")
    for cell, values in state.candidates.items():
        print(cell, "→", values)
    print("\nCandidate Singles:")
    singles = state.find_candidate_singles()
    print(singles)

    board2 = SudokuBoard(4, copy.deepcopy(grid))
    state2 = SolverState(board2)
    print("\nBefore elimination:")
    print(state2.candidates)
    changed = state2.eliminate_candidates(0,2,{2})
    print("Changed:", changed)
    print("After elimination:")
    print(state2.candidates)