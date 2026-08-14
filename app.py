from flask import Flask, render_template, request, jsonify
from sudoku.board import SudokuBoard
from sudoku.generator import generate_puzzle
from sudoku.solver import solve, count_solutions
from database import (
    get_or_create_player,
    get_best_score,
    save_best_score
)
app = Flask(__name__)
# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")
# PLAYER
@app.post("/api/player")
def create_player():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    if not username:
        return jsonify({
            "error": "Username is required."
        }), 400
    if len(username) > 50:
        return jsonify({
            "error": "Username must be 50 characters or less."
        }), 400
    try:
        player_id = get_or_create_player(username)
        return jsonify({
            "player_id": player_id,
            "username": username})
    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500
#  GET BEST SCORE\
@app.post("/api/best-score")
def best_score():
    data = request.get_json() or {}
    player_id = data.get("player_id")
    puzzle_size = data.get("puzzle_size")
    if player_id is None or puzzle_size is None:
        return jsonify({
            "error": "Player ID and puzzle size are required."
        }), 400
    try:
        player_id = int(player_id)
        puzzle_size = int(puzzle_size)
        if puzzle_size not in [4, 6, 9]:
            return jsonify({
                "error": "Unsupported Sudoku size."
            }), 400
        best_time = get_best_score(
            player_id,
            puzzle_size)
        return jsonify({
            "best_time": best_time})
    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500
# SAVE SCORE
@app.post("/api/save-score")
def save_score():
    data = request.get_json() or {}
    player_id = data.get("player_id")
    puzzle_size = data.get("puzzle_size")
    solving_time = data.get("solving_time")
    if (
        player_id is None
        or puzzle_size is None
        or solving_time is None):
        return jsonify({
            "error": (
                "Player ID, puzzle size, "
                "and solving time are required.")
        }), 400
    try:
        player_id = int(player_id)
        puzzle_size = int(puzzle_size)
        solving_time = int(solving_time)
        if puzzle_size not in [4, 6, 9]:
            return jsonify({
                "error": "Unsupported Sudoku size."
            }), 400
        if solving_time < 0:
            return jsonify({
                "error": "Invalid solving time."
            }), 400
        # Save only if this is a new personal best
        is_new_best = save_best_score(
            player_id,
            puzzle_size,
            solving_time)
        # Retrieve the actual best time
        best_time = get_best_score(
            player_id,
            puzzle_size)
        return jsonify({
            "new_best": is_new_best,
            "best_time": best_time})
    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500
# GENERATE PUZZLE
@app.post("/api/generate")
def generate():
    data = request.get_json() or {}
    size = int(data.get("size", 9))
    removals = int(data.get("removals", 40))
    if size not in [4, 6, 9]:
        return jsonify({
            "error": "Unsupported Sudoku size."
        }), 400
    try:
        board = generate_puzzle(
            size,
            removals)
        return jsonify({
            "size": board.size,
            "grid": board.grid})
    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500
# CHECK ANSWER
@app.post("/api/check")
def check_answer():
    data = request.get_json() or {}
    size = int(data["size"])
    grid = data["grid"]
    try:
        board = SudokuBoard(
            size,
            grid)
        # Validate Sudoku constraints
        if not board.validate_grid():
            return jsonify({
                "result": "invalid",
                "message": (
                    "The board contains invalid "
                    "values or conflicts.")
            })
        # Check completeness
        for row in range(size):
            for col in range(size):
                if board.grid[row][col] == 0:
                    return jsonify({
                        "result": "incomplete",
                        "message": (
                            "Fill in all the empty "
                            "cells first.")
                    })
        # Create a copy for solving
        solution_board = SudokuBoard(
            size,
            [row[:] for row in grid])
        # Verify that the submitted board represents a valid Sudoku solution
        if not solve(solution_board):
            return jsonify({
                "result": "incorrect",
                "message": (
                    "This is not a valid "
                    "Sudoku solution.")
            })
        if board.grid == solution_board.grid:
            return jsonify({
                "result": "correct",
                "message": (
                    "Congratulations! You solved "
                    "the Sudoku correctly.")
            })
        return jsonify({
            "result": "incorrect",
            "message": (
                "Some of your entries are incorrect.")
        })
    except Exception as exc:
        return jsonify({
            "result": "invalid",
            "message": str(exc)
        }), 400
# VALIDATE BOARD
@app.post("/api/validate")
def validate_board():
    data = request.get_json() or {}
    size = int(data["size"])
    grid = data["grid"]
    try:
        board = SudokuBoard(
            size,
            grid)
        if board.validate_grid():
            return jsonify({
                "valid": True,
                "message": "Board is valid."})
        return jsonify({
            "valid": False,
            "message": "Board contains conflicts."})
    except Exception as exc:
        return jsonify({
            "valid": False,
            "message": str(exc)
        }), 400
# SOLUTION COUNT
@app.post("/api/solution-count")
def solution_count():
    data = request.get_json() or {}
    size = int(data["size"])
    grid = data["grid"]
    try:
        board = SudokuBoard(
            size,
            [row[:] for row in grid])
        count = count_solutions(board)
        return jsonify({
            "count": count})
    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 400
# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)