# 🧩 Sudoku Game & Puzzle Management System

A full-stack Sudoku web application that combines **interactive gameplay**, a **Python/Flask backend**, **REST APIs**, **Sudoku solving algorithms**, and **SQL database integration**.

The application allows users to generate Sudoku puzzles of different sizes, configure puzzle difficulty, interact with generated boards, validate solutions, and manage player/game-related information through backend services.

---

## 🎯 Objective

The objective of this project is to build a complete web-based Sudoku application that demonstrates the integration of:

* Frontend web development
* Backend development using Python and Flask
* REST API development
* Algorithmic problem solving
* Sudoku puzzle generation and solving
* Client-side and server-side validation
* SQL database integration
* Modular software architecture
* Frontend-backend communication

Instead of building Sudoku as a standalone Python program, the project implements Sudoku logic as a backend service and connects it to an interactive web interface.

---

## 📌 Project Overview

The application follows a full-stack architecture where users interact with the Sudoku board through the browser.

The frontend communicates with the Flask backend using REST APIs. The backend handles:

* Puzzle generation
* Solution validation
* Player operations
* Game operations
* Database communication

### 🏗️ High-Level Architecture

```text
                    USER
                     │
                     ▼
          ┌─────────────────────┐
          │   Web Interface     │
          │    HTML / CSS / JS  │
          └──────────┬──────────┘
                     │
                     │ REST API / JSON
                     ▼
          ┌─────────────────────┐
          │    Flask Backend    │
          │      app.py         │
          └──────────┬──────────┘
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
      ┌────────┐ ┌──────────┐ ┌────────┐
      │ Board  │ │ Generator│ │ Solver │
      │ Logic  │ │  Logic   │ │ Logic  │
      └────────┘ └──────────┘ └────────┘
                     │
                     ▼
             ┌───────────────┐
             │ SQL Database  │
             │ Player / Game │
             │ Information   │
             └───────────────┘
```

---

# ✨ Key Features

## 🎮 Interactive Sudoku Gameplay

Users can interact directly with the Sudoku grid through the browser.

The application allows users to:

* Enter values into the Sudoku grid
* Modify user-entered values
* Generate new puzzles
* Select puzzle sizes
* Configure difficulty
* Submit solutions
* Receive immediate feedback

---

## 🔢 Multiple Board Sizes

The application supports multiple Sudoku board sizes:

* **4 × 4**
* **6 × 6**
* **9 × 9**

The Sudoku validation logic dynamically adapts to the selected board size.

---

## 🎚️ Adjustable Difficulty

Users can control puzzle difficulty by adjusting the number of cells removed from a completed Sudoku board.

```text
Fewer Removed Cells
        │
        ▼
   Easier Puzzle
        │
        ▼
More Removed Cells
        │
        ▼
   Harder Puzzle
```

---

## 🧠 Dynamic Sudoku Puzzle Generation

The application dynamically generates Sudoku puzzles instead of relying on predefined puzzle boards.

The generation process includes:

1. Creating a valid Sudoku solution
2. Selecting cells for removal
3. Removing values according to the selected difficulty
4. Returning the generated puzzle to the frontend

---

## ✅ Solution Validation

The application validates user-submitted Sudoku solutions according to standard Sudoku constraints.

A value is valid only when it does not violate:

* Row constraints
* Column constraints
* Sub-grid constraints

Validation is handled through the application's frontend and backend logic.

---

## 🔌 REST API

The frontend communicates with the Flask backend through REST API endpoints.

The API uses:

* HTTP requests
* JSON request bodies
* JSON responses
* POST endpoints

### Main Endpoints

| Method | Endpoint        | Purpose                          |
| ------ | --------------- | -------------------------------- |
| `POST` | `/api/generate` | Generate a Sudoku puzzle         |
| `POST` | `/api/check`    | Validate a Sudoku solution       |
| `POST` | `/api/player`   | Create/manage player information |

---

## 🗄️ SQL Database Integration

SQL is used to persist application-related information.

The database can store:

* Player information
* Game sessions
* Sudoku board size
* Difficulty
* Game status
* Scores
* Timestamps

This separates persistent application data from the Sudoku generation and solving logic.

---

# 🧩 Modular Backend

The Sudoku logic is divided into independent Python modules.

```text
sudoku/
│
├── board.py
├── generator.py
└── solver.py
```

### `board.py`

Responsible for representing and managing the Sudoku board.

### `generator.py`

Responsible for generating valid Sudoku puzzles.

### `solver.py`

Responsible for solving and validating Sudoku boards.

### `app.py`

Acts as the Flask application entry point and exposes the backend API endpoints.

---

# ⚡ Dynamic Frontend

JavaScript manages frontend interactions and communicates with the Flask backend using API requests.

The frontend handles:

* Puzzle generation
* Sudoku grid rendering
* User input
* Client-side validation
* API requests
* API responses
* Result display

The application dynamically updates the interface without requiring a complete page reload during normal gameplay.

---

# 🛠️ Tech Stack

| Technology         | Purpose                                    |
| ------------------ | ------------------------------------------ |
| **Python**         | Backend development and Sudoku algorithms  |
| **Flask**          | Web framework and REST API                 |
| **HTML5**          | Frontend structure                         |
| **CSS3**           | Styling and responsive UI                  |
| **JavaScript**     | Frontend interaction and API communication |
| **SQL**            | Data persistence                           |
| **SQLite / MySQL** | Relational database                        |
| **REST API**       | Frontend-backend communication             |
| **JSON**           | API request and response format            |
| **Git**            | Version control                            |
| **GitHub**         | Source code management                     |

> **Note:** Replace `SQLite / MySQL` with the exact database technology used in the final implementation.

---

# 🏗️ Application Architecture

The application consists of three major layers.

## 1. Frontend Layer

### Technologies

* HTML5
* CSS3
* JavaScript

### Responsibilities

* Display Sudoku board
* Accept user input
* Select puzzle size
* Select difficulty
* Generate puzzles
* Submit solutions
* Display validation results
* Communicate with REST APIs

---

## 2. Backend Layer

### Technologies

* Python
* Flask

### Responsibilities

* Generate Sudoku puzzles
* Validate Sudoku boards
* Solve Sudoku puzzles
* Handle API requests
* Process player information
* Communicate with the database
* Return JSON responses

---

## 3. Database Layer

### Technology

* SQL
* SQLite / MySQL

### Responsibilities

* Store player information
* Store game information
* Store puzzle configuration
* Store game status
* Store scores and timestamps

---

# 🗄️ Database & SQL

SQL is used to provide persistent storage for player and game-related information.

## Database Responsibilities

The database can store:

* Player information
* Game sessions
* Board size
* Difficulty
* Game status
* Score
* Creation timestamps

## Database Structure

```text
PLAYER
─────────────────────────
player_id       PRIMARY KEY
username
created_at


GAME
─────────────────────────
game_id         PRIMARY KEY
player_id       FOREIGN KEY
board_size
difficulty
status
score
created_at
```

## Example Player Table

```sql
CREATE TABLE player (
    player_id INTEGER PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Example Game Table

```sql
CREATE TABLE game (
    game_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    board_size INTEGER NOT NULL,
    difficulty INTEGER,
    status VARCHAR(50),
    score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (player_id)
        REFERENCES player(player_id)
);
```

## Example SQL Operations

### Insert Player

```sql
INSERT INTO player (username)
VALUES ('Nancy');
```

### Retrieve Players

```sql
SELECT *
FROM player;
```

### Retrieve Game History

```sql
SELECT *
FROM game
ORDER BY created_at DESC;
```

### Retrieve Games for a Player

```sql
SELECT *
FROM game
WHERE player_id = 1;
```

---

# 🧠 Sudoku Algorithm

The core Sudoku functionality is implemented using **constraint-based validation and solving techniques**.

## Board Representation

The Sudoku board is represented as a two-dimensional grid.

Example:

```text
5 3 0 | 0 7 0 | 0 0 0
6 0 0 | 1 9 5 | 0 0 0
0 9 8 | 0 0 0 | 0 6 0
------+-------+------
8 0 0 | 0 6 0 | 0 0 3
4 0 0 | 8 0 3 | 0 0 1
7 0 0 | 0 2 0 | 0 0 6
------+-------+------
0 6 0 | 0 0 0 | 2 8 0
0 0 0 | 4 1 9 | 0 0 5
0 0 0 | 0 8 0 | 0 7 9
```

> `0` represents an empty cell.

---

## Sudoku Validation

Before placing a value in an empty cell, the application checks:

```text
             Candidate Value
                    │
          ┌─────────┼─────────┐
          │         │         │
          ▼         ▼         ▼
        Row       Column    Sub-grid
       Check       Check      Check
          │         │         │
          └─────────┼─────────┘
                    │
                    ▼
             Valid / Invalid
```

A value is valid only when it does not already exist in:

* The same row
* The same column
* The corresponding sub-grid

---

## Puzzle Solving

The solver searches for valid values for empty cells while respecting Sudoku constraints.

The solver can be used to:

* Solve Sudoku boards
* Validate generated puzzles
* Verify user solutions
* Ensure generated boards follow Sudoku rules

---

# 🔌 REST API

The frontend communicates with the Flask backend through REST API endpoints.

## Generate Puzzle

### Endpoint

```http
POST /api/generate
```

### Request

```json
{
    "size": 9,
    "removals": 45
}
```

### Parameters

| Parameter  | Description             |
| ---------- | ----------------------- |
| `size`     | Sudoku board size       |
| `removals` | Number of cells removed |

---

## Check Answer

### Endpoint

```http
POST /api/check
```

### Request

```json
{
    "size": 9,
    "grid": [
        [5, 3, 4, 6, 7, 8, 9, 1, 2]
    ]
}
```

The backend validates the submitted Sudoku grid and returns the validation result.

---

## Player API

### Create Player

```http
POST /api/player
```

### Request

```json
{
    "username": "Nancy"
}
```

The player information can then be stored in the SQL database.

---

# 🔄 Application Workflow

```text
                  USER OPENS APPLICATION
                           │
                           ▼
                 SELECT SUDOKU SIZE
                           │
                           ▼
                 SELECT DIFFICULTY
                           │
                           ▼
                GENERATE PUZZLE
                           │
                           ▼
                 FRONTEND REQUEST
                           │
                           ▼
                  FLASK BACKEND
                           │
                           ▼
                SUDOKU GENERATOR
                           │
                           ▼
                 VALID PUZZLE
                           │
                           ▼
                  JSON RESPONSE
                           │
                           ▼
                DISPLAY PUZZLE
                           │
                           ▼
                  USER SOLVES
                           │
                           ▼
                 SUBMIT ANSWER
                           │
                           ▼
               BACKEND VALIDATION
                           │
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
                 CORRECT       INCORRECT
                    │             │
                    └──────┬──────┘
                           │
                           ▼
                  GAME INFORMATION
                           │
                           ▼
                    SQL DATABASE
```

---

# 📂 Project Structure

```text
SUDOKU-HTML/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── sudoku/
│   ├── __init__.py
│   ├── board.py
│   ├── generator.py
│   └── solver.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── app.js
│   │
│   ├── image.png
│   └── image2.png
│
├── templates/
│   └── index.html
│
├── database/
│   └── ...
│
└── screenshots/
    ├── 01-main-interface.png
    ├── 02-generated-puzzle.png
    ├── 03-solution-validation.png
    ├── 04-player-management.png
    └── 05-database.png
```

---

# 📸 Screenshots

## 🏠 Main Application

The main interface provides the Sudoku game controls, board size selection, difficulty configuration, and interactive Sudoku grid.

## 🧩 Generated Sudoku Puzzle

The application dynamically generates a Sudoku puzzle according to the selected board size and difficulty.

## ✅ Solution Validation

The application validates the user's submitted solution and displays the corresponding result.

## 👤 Player Management

Player-related information can be managed through the backend API and persisted in the SQL database.

## 🗄️ Database

The database stores persistent player and game-related information.

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate the environment:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the Database

Configure the SQL database according to the project's database implementation.

### For SQLite

The database can be created locally by the application.

### For MySQL

Configure the database connection and credentials in the application configuration.

> **Important:** Do not commit database credentials or `.env` files to GitHub.

## 5. Run the Application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

# 🧪 API Testing

The REST API can be tested using:

* Postman
* Python `requests`
* cURL
* Browser Developer Tools

### Example Using Python

```python
import requests

BASE_URL = "http://127.0.0.1:5000"

response = requests.post(
    f"{BASE_URL}/api/player",
    json={
        "username": "Nancy"
    }
)

print(response.json())
```

---

# 🔐 Configuration & Security

Sensitive information should not be stored directly in the source code.

Examples include:

* Database passwords
* API keys
* Secret keys
* Environment-specific configuration

Use environment variables or a `.env` file for sensitive configuration.

The `.env` file should be excluded from version control using `.gitignore`.

---

# 📊 Skills Demonstrated

## Programming

* Python
* Object-Oriented Programming
* Data Structures
* Algorithm Design
* Constraint-Based Problem Solving
* Exception Handling

## Backend Development

* Flask
* REST API Development
* HTTP Requests
* JSON
* Backend Validation
* API Integration

## Frontend Development

* HTML5
* CSS3
* JavaScript
* DOM Manipulation
* Fetch API
* Responsive UI

## Database

* SQL
* Relational Database Design
* CRUD Operations
* Primary Keys
* Foreign Keys
* Database Connectivity
* Data Persistence

## Software Engineering

* Modular Architecture
* Separation of Concerns
* Client-Server Architecture
* RESTful Communication
* Version Control
* Git
* GitHub

---

# 📈 Future Enhancements

Potential future improvements include:

* 👤 User authentication
* 🏆 Leaderboards
* 📊 Player performance analytics
* ⏱️ Game timer
* 💡 Sudoku hint system
* 🏅 Difficulty-based scoring
* 💾 Saved games
* 📜 Game history
* 📱 Improved mobile responsiveness
* ☁️ Cloud deployment
* 🗄️ Advanced database analytics

---

# 🎯 Project Outcome

This project demonstrates how an algorithmic problem can be transformed into a complete full-stack web application.

```text
Python
    +
Sudoku Algorithms
    +
Flask Backend
    +
REST APIs
    +
HTML / CSS / JavaScript
    +
SQL Database
    =
Full-Stack Sudoku Application
```

The project provides practical experience in:

* Backend development
* Frontend development
* Algorithm design
* REST API integration
* SQL database management
* Client-server architecture
* Modular software development
* Version control

---

# 👨‍💻 Author

**Chhandavi Gowardhan**

*Aspiring Data Analyst | AI & ML Enthusiast | Python Developer*

---

# ⭐ Support

If you found this project useful or interesting, consider giving the repository a ⭐ on GitHub.
