from sudoku.board import SudokuBoard
from sudoku.difficulty import (
    find_naked_pairs,
    find_pointing_pairs,
    eliminate_pointing_pair,)
from sudoku.logical_solver import LogicalSolver
from sudoku.generator import generate_solution, generate_puzzle
from sudoku.solver import count_solutions
def test_naked_pair_detection():
    board = SudokuBoard(4,
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],],)
    candidates = {
        (0, 0): {1, 2},
        (0, 1): {1, 2},
        (0, 2): {1, 2, 3},
        (0, 3): {1, 2, 3, 4},}
    pairs = find_naked_pairs(board, candidates)
    assert len(pairs) > 0
    found_pair = False
    for cells, locations, numbers in pairs:
        if (
            set(locations) == {(0, 0), (0, 1)}
            and numbers == frozenset({1, 2})):
            found_pair = True
            break
    assert found_pair
def test_pointing_pair_detection():
    board = SudokuBoard(4,
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],],)
    candidates = {
        (0, 0): {1, 2},
        (0, 1): {2, 3},
        (1, 0): {1, 3},
        (1, 1): {2, 3},
        (2, 0): {1, 2, 3, 4},
        (3, 0): {1, 2, 3, 4},
        (2, 1): {1, 2, 3, 4},
        (3, 1): {1, 2, 3, 4},
        (2, 2): {1, 2, 3, 4},
        (2, 3): {1, 2, 3, 4},
        (3, 2): {1, 2, 3, 4},
        (3, 3): {1, 2, 3, 4},}
    pairs = find_pointing_pairs(board, candidates)
    assert len(pairs) > 0
    found_pointing_pair = False
    for pair in pairs:
        if (
            pair["box"] == (0, 0)
            and pair["number"] == 1
            and pair["direction"] == "column"):
            found_pointing_pair = True
            break
    assert found_pointing_pair
def test_pointing_pair_elimination():
    board = SudokuBoard(4,
        [
            [0, 0, 0, 4],
            [3, 4, 0, 2],
            [2, 0, 4, 3],
            [4, 3, 2, 1],],)
    candidates = {
        (0, 0): {1},
        (0, 1): {1, 2},
        (0, 2): {1, 3},
        (1, 2): {1},
        (2, 1): {1},}
    pairs = find_pointing_pairs(board, candidates)
    assert len(pairs) > 0
    applied = False
    for pair in pairs:
        changes = eliminate_pointing_pair(
            board,
            candidates,
            pair["box"],
            pair["number"],
            pair["direction"],
            pair["source_cells"],)
        if changes:
            applied = True
            break
    assert applied
    assert candidates[(0, 2)] == {3}
def test_logical_solver_solves_simple_puzzle():
    board = SudokuBoard(4,
        [
            [1, 2, 3, 0],
            [3, 0, 1, 2],
            [0, 1, 2, 3],
            [2, 3, 0, 1],],)
    solver = LogicalSolver(board)
    solved = solver.solve()
    assert solved is True
    assert solver.state.is_solved()
def test_logical_solver_tracks_naked_singles():
    board = SudokuBoard(4,
        [
            [1, 2, 3, 0],
            [3, 0, 1, 2],
            [0, 1, 2, 3],
            [2, 3, 0, 1],],)
    solver = LogicalSolver(board)
    solver.solve()
    assert solver.techniques_used["naked_single"] > 0
    assert solver.placements > 0
def test_logical_solver_summary():
    board = SudokuBoard(4,[
            [1, 2, 3, 0],
            [3, 0, 1, 2],
            [0, 1, 2, 3],
            [2, 3, 0, 1],],)
    solver = LogicalSolver(board)
    solver.solve()
    summary = solver.get_summary()
    assert summary["solved"] is True
    assert summary["steps"] > 0
    assert summary["placements"] > 0
    assert "techniques" in summary
def test_generate_solution_is_complete_and_valid():
    board = generate_solution(4)
    assert board.find_empty() is None
    assert board.validate_grid() is True
def test_generate_puzzle_has_requested_removals():
    removals = 6
    board = generate_puzzle(4, removals)
    empty_cells = sum(
        1
        for row in range(board.size)
        for col in range(board.size)
        if board.is_empty(row, col)
    )
    assert empty_cells == removals
    assert board.validate_grid() is True
def test_generate_puzzle_has_unique_solution():
    board = generate_puzzle(4, 6)
    assert count_solutions(board) == 1