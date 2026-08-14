import requests


BASE_URL = "http://127.0.0.1:5000"


# ============================================================
# TEST 1: CREATE PLAYER
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/player",
    json={
        "username": "Nancy"
    }
)

print("\nCREATE PLAYER")
print(response.status_code)
print(response.json())

player_data = response.json()
player_id = player_data["player_id"]


# ============================================================
# TEST 2: GET INITIAL BEST SCORE
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/best-score",
    json={
        "player_id": player_id,
        "puzzle_size": 4
    }
)

print("\nGET INITIAL BEST SCORE")
print(response.status_code)
print(response.json())


# ============================================================
# TEST 3: SAVE FIRST SCORE
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/save-score",
    json={
        "player_id": player_id,
        "puzzle_size": 4,
        "solving_time": 40
    }
)

print("\nSAVE FIRST SCORE (40 seconds)")
print(response.status_code)
print(response.json())


# ============================================================
# TEST 4: GET BEST SCORE AFTER FIRST SCORE
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/best-score",
    json={
        "player_id": player_id,
        "puzzle_size": 4
    }
)

print("\nGET BEST SCORE AFTER FIRST SCORE")
print(response.status_code)
print(response.json())


# ============================================================
# TEST 5: TRY A WORSE SCORE
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/save-score",
    json={
        "player_id": player_id,
        "puzzle_size": 4,
        "solving_time": 90
    }
)

print("\nSAVE WORSE SCORE (90 seconds)")
print(response.status_code)
print(response.json())


# ============================================================
# TEST 6: VERIFY WORSE SCORE DID NOT REPLACE BEST
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/best-score",
    json={
        "player_id": player_id,
        "puzzle_size": 4
    }
)

print("\nVERIFY BEST SCORE AFTER WORSE SCORE")
print(response.status_code)
print(response.json())


# ============================================================
# TEST 7: TRY A BETTER SCORE
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/save-score",
    json={
        "player_id": player_id,
        "puzzle_size": 4,
        "solving_time": 30
    }
)

print("\nSAVE BETTER SCORE (30 seconds)")
print(response.status_code)
print(response.json())


# ============================================================
# TEST 8: VERIFY BETTER SCORE BECAME NEW BEST
# ============================================================

response = requests.post(
    f"{BASE_URL}/api/best-score",
    json={
        "player_id": player_id,
        "puzzle_size": 4
    }
)

print("\nFINAL BEST SCORE")
print(response.status_code)
print(response.json())