import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"))
def get_or_create_player(username):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Check if player already exists
        cursor.execute(
            "SELECT id FROM players WHERE username = %s",
            (username,))
        player = cursor.fetchone()
        if player:
            return player[0]
        # Create new player
        cursor.execute(
            "INSERT INTO players (username) VALUES (%s)",
            (username,))
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()
def get_best_score(player_id, puzzle_size):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT best_time
            FROM best_scores
            WHERE player_id = %s
              AND puzzle_size = %s
            """,
            (player_id, puzzle_size))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    finally:
        cursor.close()
        connection.close()
def save_best_score(player_id, puzzle_size, solving_time):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        current_best = get_best_score(
            player_id,
            puzzle_size)
        # No previous score → create one
        if current_best is None:
            cursor.execute(
                """
                INSERT INTO best_scores
                (player_id, puzzle_size, best_time)
                VALUES (%s, %s, %s)
                """,
                (
                    player_id,
                    puzzle_size,
                    solving_time))
            connection.commit()
            return True
        # New score is better → update it
        if solving_time < current_best:
            cursor.execute(
                """
                UPDATE best_scores
                SET best_time = %s
                WHERE player_id = %s
                  AND puzzle_size = %s
                """,
                (
                    solving_time,
                    player_id,
                    puzzle_size)
            )
            connection.commit()
            return True
        # Existing score is already better
        return False
    finally:
        cursor.close()
        connection.close()