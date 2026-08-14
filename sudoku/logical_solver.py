from .solver_state import SolverState
from .difficulty import (
    find_naked_pairs,
    find_pointing_pairs,
    eliminate_pointing_pair)
from .board import SudokuBoard
from .difficulty_rating import rate_solver

class LogicalSolver:
    def __init__(self, board):
        self.state = SolverState(board)
        self.techniques_used = {
            "naked_single": 0,
            "hidden_single": 0,
            "naked_pair": 0, 
            "pointing_pair": 0}
        self.steps = [] 
        self.placements = 0   
    def apply_naked_singles(self):
        singles = self.state.find_candidate_singles()
        if not singles:
            return False
        row, col, number = singles[0]
        self.state.place_number(row, col, number)
        self.placements += 1
        self.techniques_used["naked_single"] += 1
        self.steps.append({
        "technique": "naked_single",
        "row": row,
        "col": col,
        "number": number})
        return True
    def find_hidden_singles(self):
        singles = []
        candidates = self.state.candidates
        board = self.state.board
        # Rows
        for row in range(board.size):
            locations = {}
            for col in range(board.size):
                cell = (row, col)
                if cell not in candidates:
                    continue
                for number in candidates[cell]:
                    if number not in locations:
                        locations[number] = []
                    locations[number].append(cell)
            for number, cells in locations.items():
                if len(cells) == 1:
                    row_pos, col_pos = cells[0]
                    singles.append(
                        (row_pos, col_pos, number)
                    )
        # Columns
        for col in range(board.size):
            locations = {}
            for row in range(board.size):
                cell = (row, col)
                if cell not in candidates:
                    continue
                for number in candidates[cell]:
                    if number not in locations:
                        locations[number] = []
                    locations[number].append(cell)
            for number, cells in locations.items():
                if len(cells) == 1:
                    row_pos, col_pos = cells[0]
                    singles.append(
                        (row_pos, col_pos, number)
                    )
        # Boxes
        for box_row in range(
            0,
            board.size,
            board.box_rows):
            for box_col in range(
                0,
                board.size,
                board.box_cols):
                locations = {}
                for row in range(
                    box_row,
                    box_row + board.box_rows):
                    for col in range(
                        box_col,
                        box_col + board.box_cols):
                        cell = (row, col)
                        if cell not in candidates:
                            continue
                        for number in candidates[cell]:
                            if number not in locations:
                                locations[number] = []
                            locations[number].append(cell)
                for number, cells in locations.items():
                    if len(cells) == 1:
                        row_pos, col_pos = cells[0]
                        singles.append(
                            (row_pos, col_pos, number)
                        )
        return singles
    def apply_hidden_singles(self):
        singles = self.find_hidden_singles()
        if not singles:
            return False
        row, col, number = singles[0]
        self.state.place_number(
            row,
            col,
            number)
        self.placements += 1
        self.techniques_used[
            "hidden_single"] += 1
        self.steps.append({
            "technique": "hidden_single",
            "row": row,
            "col": col,
            "number": number})
        return True
    
    def apply_naked_pairs(self):
        pairs = find_naked_pairs(
           self.state.board,
            self.state.candidates)
        for cells, pair_locations, pair_numbers in pairs:
            pair_cells = set(pair_locations)
            eliminations = []
            for row, col in cells:
                if (row, col) in pair_cells:
                    continue
                if (row, col) not in self.state.candidates:
                    continue
                old_candidates = self.state.candidates[
                    (row, col)
                ].copy()
                changed = self.state.eliminate_candidates(
                    row,
                    col,
                    pair_numbers
                )
                if changed:
                    new_candidates = self.state.candidates[
                        (row, col)
                    ].copy()
                    eliminations.append({
                        "cell": (row, col),
                        "removed": old_candidates - new_candidates,
                        "before": old_candidates,
                        "after": new_candidates
                    })
            if eliminations:
                self.techniques_used[
                    "naked_pair"
                ] += 1
                self.steps.append({
                    "technique": "naked_pair",
                    "pair_cells": pair_locations,
                    "pair_numbers": pair_numbers,
                    "eliminations": eliminations
                })
                return True
        return False

    def apply_pointing_pairs(self):
        pairs = find_pointing_pairs(
            self.state.board,
            self.state.candidates)
        for pair in pairs:
            box = pair["box"]
            number = pair["number"]
            direction = pair["direction"]
            source_cells = pair["source_cells"]
            changes = eliminate_pointing_pair(
                self.state.board,
                self.state.candidates,
                box,
                number,
                direction,
                source_cells)
            if changes:
                self.techniques_used["pointing_pair"] += 1
                self.steps.append({
                    "technique": "pointing_pair",
                    "box": box,
                    "number": number,
                    "direction": direction,
                    "source_cells": source_cells,
                    "eliminations": changes})
                return True
        return False

    def solve(self):
        while True:
            if self.state.is_solved():
                return True
            if self.apply_naked_singles():
                continue
            if self.apply_hidden_singles():
                continue
            if self.apply_naked_pairs():
                continue
            if self.apply_pointing_pairs():
                continue
            break
        return self.state.is_solved()

    def get_summary(self):
        return {
            "solved": self.state.is_solved(),
            "steps": len(self.steps),
            "placements": self.placements,
            "techniques": self.techniques_used.copy()
        }

    def get_progress(self):
        remaining_empty = 0
        board = self.state.board
        for row in range(board.size):
            for col in range(board.size):
                if board.is_empty(row, col):
                   remaining_empty += 1
        total_empty = self.placements + remaining_empty
        if total_empty == 0:
            return 1.0
        return self.placements / total_empty

if __name__ == "__main__":
    grid = [
    [1, 2, 3, 0],
    [3, 0, 1, 2],
    [0, 1, 2, 3],
    [2, 3, 0, 1]]
    board = SudokuBoard(4, grid)
    print("Original:")
    board.display()
    solver = LogicalSolver(board)
    solved = solver.solve()
    print("\nSolved:", solved)
    print("\nFinal board:")
    board.display()
    print("\nTechniques used:")
    print(solver.techniques_used)
    print("\nSolving steps:")
    for step in solver.steps:
        print(step)
    print("\nSummary:")
    print(solver.get_summary())
    print("\nProgress:")
    print(solver.get_progress())
    print("\nDifficulty:")
    rating = rate_solver(solver.get_summary())
    print("Score:", rating["score"])
    print("Level:", rating["level"])