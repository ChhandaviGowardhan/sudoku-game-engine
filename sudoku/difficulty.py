from .board import SudokuBoard

def get_candidates(board, row, col):
    """Return valid candidates for an empty cell."""
    if not board.is_empty(row, col):
        return set()
    candidates = set(range(1, board.size + 1))
    # Row
    for value in board.grid[row]:
        candidates.discard(value)
    # Column
    for r in range(board.size):
        candidates.discard(board.grid[r][col])
    # Box
    box_start_row = (row // board.box_rows) * board.box_rows
    box_start_col = (col // board.box_cols) * board.box_cols
    for r in range(
        box_start_row,
        box_start_row + board.box_rows):
        for c in range(
            box_start_col,
            box_start_col + board.box_cols):
            candidates.discard(board.grid[r][c])
    return candidates
def build_candidates(board):
    """Build candidate sets for all empty cells."""
    candidates = {}
    for row in range(board.size):
        for col in range(board.size):
            if board.is_empty(row, col):
                candidates[(row, col)] = get_candidates(
                    board, row, col)
    return candidates
def find_naked_pairs_in_unit(cells, candidates):
    """Find naked pairs inside one row, column, or box."""
    pairs = []
    candidate_map = {}
    for cell in cells:
        if cell not in candidates:
            continue
        possible_numbers = candidates[cell]
        if len(possible_numbers) == 2:
            key = frozenset(possible_numbers)
            if key not in candidate_map:
                candidate_map[key] = []
            candidate_map[key].append(cell)
    for pair_numbers, locations in candidate_map.items():
        if len(locations) == 2:
            pairs.append(
                (cells, locations, pair_numbers))
    return pairs
def find_naked_pairs_in_rows(board, candidates):
    pairs = []
    for row in range(board.size):
        cells = [
            (row, col)
            for col in range(board.size)]
        pairs.extend(
            find_naked_pairs_in_unit(
                cells,
                candidates))
    return pairs
def find_naked_pairs_in_columns(board, candidates):
    pairs = []
    for col in range(board.size):
        cells = [
            (row, col)
            for row in range(board.size)]
        pairs.extend(
            find_naked_pairs_in_unit(
                cells,
                candidates))
    return pairs
def find_naked_pairs_in_boxes(board, candidates):
    pairs = []
    for box_row in range(
        0,
        board.size,
        board.box_rows):
        for box_col in range(
            0,
            board.size,
            board.box_cols):
            cells = []
            for row in range(
                box_row,
                box_row + board.box_rows):
                for col in range(
                    box_col,
                    box_col + board.box_cols):
                    cells.append((row, col))
            pairs.extend(
                find_naked_pairs_in_unit(
                    cells,
                    candidates)
            )
    return pairs
def find_naked_pairs(board, candidates):
    """Find all naked pairs."""
    pairs = []
    pairs.extend(
        find_naked_pairs_in_rows(
            board,
            candidates)
    )
    pairs.extend(
        find_naked_pairs_in_columns(
            board,
            candidates)
    )
    pairs.extend(
        find_naked_pairs_in_boxes(
            board,
            candidates)
    )
    return pairs
def eliminate_naked_pair_from_unit(
    candidates,
    cells,
    pair_locations,
    pair_numbers):
    """Remove naked-pair numbers from other cells."""
    changes = []
    pair_cells = set(pair_locations)
    for cell in cells:
        if cell in pair_cells:
            continue
        if cell not in candidates:
            continue
        old_candidates = candidates[cell].copy()
        candidates[cell] -= pair_numbers
        if candidates[cell] != old_candidates:
            changes.append({
                "cell": cell,
                "removed": (
                    old_candidates - candidates[cell]),
                "before": old_candidates,
                "after": candidates[cell].copy()})
    return changes
def find_pointing_pairs(board, candidates):
    """Find candidates confined to one row/column inside a box."""
    pointing_pairs = []
    for box_row in range(
        0,
        board.size,
        board.box_rows):
        for box_col in range(
            0,
            board.size,
            board.box_cols):
            box_cells = []
            for row in range(
                box_row,
                box_row + board.box_rows):
                for col in range(
                    box_col,
                    box_col + board.box_cols):
                    cell = (row, col)
                    if cell in candidates:
                        box_cells.append(cell)
            for number in range(1, board.size + 1):
                locations = []
                for cell in box_cells:
                    if number in candidates[cell]:
                        locations.append(cell)
                if len(locations) < 2:
                    continue
                rows = {
                    row
                    for row, col in locations}
                cols = {
                    col
                    for row, col in locations}
                # Candidate confined to one row
                if len(rows) == 1:
                    pointing_pairs.append({
                        "box": (
                            box_row,
                            box_col),
                        "number": number,
                        "direction": "row",
                        "source_cells": locations})
                # Candidate confined to one column
                if len(cols) == 1:
                    pointing_pairs.append({
                        "box": (
                            box_row,
                            box_col),
                        "number": number,
                        "direction": "column",
                        "source_cells": locations})
    return pointing_pairs
def eliminate_pointing_pair(
    board,
    candidates,
    box,
    number,
    direction,
    source_cells):
    """Remove a pointing-pair candidate outside its box."""
    changes = []
    source_cells = set(source_cells)
    if direction == "row":
        row = next(iter(source_cells))[0]
        for col in range(board.size):
            cell = (row, col)
            # Don't modify the source cells.
            if cell in source_cells:
                continue
            if cell not in candidates:
                continue
            if number not in candidates[cell]:
                continue
            before = candidates[cell].copy()
            candidates[cell].discard(number)
            after = candidates[cell].copy()
            if before != after:
                changes.append({
                    "cell": cell,
                    "removed": before - after,
                    "before": before,
                    "after": after})
    elif direction == "column":
        col = next(iter(source_cells))[1]
        for row in range(board.size):
            cell = (row, col)
            # Don't modify the source cells.
            if cell in source_cells:
                continue
            if cell not in candidates:
                continue
            if number not in candidates[cell]:
                continue
            before = candidates[cell].copy()
            candidates[cell].discard(number)
            after = candidates[cell].copy()
            if before != after:
                changes.append({
                    "cell": cell,
                    "removed": before - after,
                    "before": before,
                    "after": after})
    return changes