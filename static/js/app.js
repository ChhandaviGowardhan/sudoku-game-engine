let board = null;
let originalBoard = null;
let selectedCell = null;
let timerInterval = null;
let startTime = null;
let puzzleSize = 9;
let playerId = null;
let username = null;
// DOM ELEMENTS
const sizeSelect = document.getElementById("size");
const removalsSlider = document.getElementById("removals");
const removalsValue = document.getElementById("removals-value");
const generateButton = document.getElementById("generate-btn");
const boardElement = document.getElementById("sudoku-board");
const numberPad = document.getElementById("number-pad");
const clearButton = document.getElementById("clear-btn");
const checkButton = document.getElementById("check-btn");
const resetButton = document.getElementById("reset-btn");
const timerElement = document.getElementById("timer");
const messageElement = document.getElementById("message");
const usernameInput = document.getElementById("username");
const playerButton = document.getElementById("player-btn");
const playerMessage = document.getElementById("player-message");
const bestTimeElement = document.getElementById("best-time");
// PLAYER
playerButton.addEventListener(
    "click",
    createPlayer);
async function createPlayer() {
    const enteredUsername = usernameInput.value.trim();
    if (!enteredUsername) {
        playerMessage.textContent =
            "Please enter your name.";
        return;}
    try {
        const response =
            await fetch("/api/player", {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"},
                body: JSON.stringify({
                    username: enteredUsername
                })
            });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(
                data.error ||
                "Unable to create player.");
        }
        // Store player information
        playerId = data.player_id;
        username = data.username;
        playerMessage.textContent =
        `Welcome, ${username}!`;
console.log(
    "Player created:",
    playerId,
    username);
await loadBestScore();}
    catch (error) {
        console.error(
            "Player creation error:",
            error);
        playerMessage.textContent =
            error.message;}
}
// LOAD BEST SCORE
async function loadBestScore() {
    if (!playerId) {
        return;}
    try {
        const response =
            await fetch("/api/best-score", {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"},
                body: JSON.stringify({
                    player_id: playerId,
                    puzzle_size: puzzleSize})
            });
        const data =
            await response.json();
        if (!response.ok) {
            throw new Error(
                data.error ||
                "Unable to load best score.");
        }
        if (data.best_time === null) {
            bestTimeElement.textContent =
                "--:--";
        } else {
            bestTimeElement.textContent =
                formatTime(data.best_time);}
        console.log(
            "Best score:",
            data.best_time);
    }
    catch (error) {
        console.error(
            "Best score error:",
            error);
        bestTimeElement.textContent =
            "--:--";}
}
// DISPLAY BEST TIME
function displayBestTime(bestTime) {
    if (!bestTimeElement) {
        console.warn(
            "Element with id 'best-time' was not found.");
        return;}
    if (bestTime === null) {
        bestTimeElement.textContent =
            "--:--";
        return;}
    bestTimeElement.textContent =
        formatTime(bestTime);}
// DEFAULT REMOVAL VALUES
const removalOptions = {
    4: {
        min: 4,
        max: 8,
        value: 6},
    6: {
        min: 10,
        max: 20,
        value: 15},
    9: {
        min: 30,
        max: 50,
        value: 40}
    };
// SIZE CHANGE
sizeSelect.addEventListener(
    "change",
    () => {

        puzzleSize =
            Number(sizeSelect.value);


        const options =
            removalOptions[puzzleSize];


        removalsSlider.min =
            options.min;

        removalsSlider.max =
            options.max;

        removalsSlider.value =
            options.value;

        removalsValue.textContent =
            options.value;


        clearBoard();
        stopTimer();
        timerElement.textContent = "00:00";
        // Load best score for selected puzzle size
        if (playerId) {
            loadBestScore();}
    }
);
removalsSlider.addEventListener(
    "input",
    () => {

        removalsValue.textContent =
            removalsSlider.value;

    }
);


// ============================================================
// GENERATE PUZZLE
// ============================================================

generateButton.addEventListener(
    "click",
    generatePuzzle
);


async function generatePuzzle() {

    puzzleSize =
        Number(sizeSelect.value);


    const removals =
        Number(removalsSlider.value);


    showMessage(
        "Generating puzzle...",
        "warning"
    );


    try {

        const response =
            await fetch("/api/generate", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    size:
                        puzzleSize,

                    removals:
                        removals

                })
            });


        const data =
            await response.json();


        console.log(
            "Generate API response:",
            data
        );


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Failed to generate puzzle."
            );
        }


        // ------------------------------------------------
        // Store puzzle
        // ------------------------------------------------

        board =
            data.grid.map(
                row => [...row]
            );


        originalBoard =
            data.grid.map(
                row => [...row]
            );


        selectedCell = null;


        // ------------------------------------------------
        // Render puzzle
        // ------------------------------------------------

        renderBoard();

        renderNumberPad();

        hideMessage();

        startTimer();

    }

    catch (error) {

        console.error(
            "Generate puzzle error:",
            error
        );

        showMessage(
            error.message,
            "error"
        );
    }
}


// ============================================================
// RENDER BOARD
// ============================================================

function renderBoard() {

    boardElement.innerHTML = "";


    boardElement.style.gridTemplateColumns =
        `repeat(${puzzleSize}, 1fr)`;


    for (
        let row = 0;
        row < puzzleSize;
        row++
    ) {

        for (
            let col = 0;
            col < puzzleSize;
            col++
        ) {

            const cell =
                document.createElement("div");


            cell.classList.add(
                "cell"
            );


            const value =
                board[row][col];


            // ------------------------------------------------
            // GIVEN / USER CELLS
            // ------------------------------------------------

            if (
                originalBoard[row][col] !== 0
            ) {

                cell.classList.add(
                    "given"
                );

            }

            else {

                cell.classList.add(
                    "user-filled"
                );


                cell.addEventListener(
                    "click",
                    () =>
                        selectCell(row, col)
                );
            }


            // ------------------------------------------------
            // SELECTED CELL
            // ------------------------------------------------

            if (
                selectedCell &&
                selectedCell.row === row &&
                selectedCell.col === col
            ) {

                cell.classList.add(
                    "selected"
                );
            }


            // ------------------------------------------------
            // CELL VALUE
            // ------------------------------------------------

            if (value !== 0) {

                cell.textContent =
                    value;

            }

            else {

                cell.textContent =
                    "";
            }


            // ========================================================
            // SUDOKU BOX BORDERS
            // ========================================================

            let boxRows;
            let boxCols;


            if (puzzleSize === 9) {

                boxRows = 3;
                boxCols = 3;

            }

            else if (puzzleSize === 6) {

                boxRows = 2;
                boxCols = 3;

            }

            else {

                boxRows = 2;
                boxCols = 2;
            }


            // ------------------------------------------------
            // Vertical box separation
            // ------------------------------------------------

            if (
                (col + 1) % boxCols === 0 &&
                col < puzzleSize - 1
            ) {

                cell.style.borderRight =
                    "3px solid #111827";
            }


            // ------------------------------------------------
            // Horizontal box separation
            // ------------------------------------------------

            if (
                (row + 1) % boxRows === 0 &&
                row < puzzleSize - 1
            ) {

                cell.style.borderBottom =
                    "3px solid #111827";
            }


            boardElement.appendChild(
                cell
            );
        }
    }
}


// ============================================================
// SELECT CELL
// ============================================================

function selectCell(row, col) {

    if (
        originalBoard[row][col] !== 0
    ) {

        return;
    }


    selectedCell = {

        row:
            row,

        col:
            col

    };


    renderBoard();
}


// ============================================================
// NUMBER PAD
// ============================================================

function renderNumberPad() {

    numberPad.innerHTML = "";


    for (
        let number = 1;
        number <= puzzleSize;
        number++
    ) {

        const button =
            document.createElement("button");


        button.textContent =
            number;


        button.classList.add(
            "number-button"
        );


        button.addEventListener(
            "click",
            () =>
                enterNumber(number)
        );


        numberPad.appendChild(
            button
        );
    }
}


// ============================================================
// ENTER NUMBER
// ============================================================

function enterNumber(number) {

    if (!selectedCell) {

        showMessage(
            "Select an empty cell first.",
            "warning"
        );

        return;
    }


    const row =
        selectedCell.row;


    const col =
        selectedCell.col;


    // ------------------------------------------------
    // Frontend validation
    // ------------------------------------------------

    if (
        !isValidMove(
            row,
            col,
            number
        )
    ) {

        showMessage(
            `${number} cannot be placed here.`,
            "error"
        );

        return;
    }


    board[row][col] =
        number;


    selectedCell = null;


    renderBoard();


    hideMessage();
}


// ============================================================
// FRONTEND VALIDATION
// ============================================================

function isValidMove(
    row,
    col,
    number
) {

    // ------------------------------------------------
    // Row
    // ------------------------------------------------

    for (
        let colIndex = 0;
        colIndex < puzzleSize;
        colIndex++
    ) {

        if (
            colIndex !== col &&
            board[row][colIndex] === number
        ) {

            return false;
        }
    }


    // ------------------------------------------------
    // Column
    // ------------------------------------------------

    for (
        let rowIndex = 0;
        rowIndex < puzzleSize;
        rowIndex++
    ) {

        if (
            rowIndex !== row &&
            board[rowIndex][col] === number
        ) {

            return false;
        }
    }


    // ------------------------------------------------
    // Box dimensions
    // ------------------------------------------------

    let boxRows;
    let boxCols;


    if (puzzleSize === 9) {

        boxRows = 3;
        boxCols = 3;

    }

    else if (puzzleSize === 6) {

        boxRows = 2;
        boxCols = 3;

    }

    else {

        boxRows = 2;
        boxCols = 2;
    }


    const startRow =
        Math.floor(row / boxRows) *
        boxRows;


    const startCol =
        Math.floor(col / boxCols) *
        boxCols;


    for (
        let r = startRow;
        r < startRow + boxRows;
        r++
    ) {

        for (
            let c = startCol;
            c < startCol + boxCols;
            c++
        ) {

            if (
                (r !== row || c !== col) &&
                board[r][c] === number
            ) {

                return false;
            }
        }
    }


    return true;
}


// ============================================================
// CLEAR CELL
// ============================================================

clearButton.addEventListener(
    "click",
    clearSelectedCell
);


function clearSelectedCell() {

    if (!selectedCell) {

        showMessage(
            "Select an editable cell first.",
            "warning"
        );

        return;
    }


    const row =
        selectedCell.row;


    const col =
        selectedCell.col;


    if (
        originalBoard[row][col] !== 0
    ) {

        return;
    }


    board[row][col] = 0;


    selectedCell = null;


    renderBoard();


    hideMessage();
}


// ============================================================
// CHECK ANSWER
// ============================================================

checkButton.addEventListener(
    "click",
    checkAnswer
);


async function checkAnswer() {

    if (!board) {

        showMessage(
            "Generate a puzzle first.",
            "warning"
        );

        return;
    }

    if (!playerId) {

        showMessage(
            "Please enter your player name first.",
            "warning"
        );

        return;
    }

    try {

        // ====================================================
        // CHECK THE SOLUTION
        // ====================================================

        const response =
            await fetch("/api/check", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    size: puzzleSize,
                    grid: board
                })

            });

        const data =
            await response.json();

        // ====================================================
        // INCOMPLETE
        // ====================================================

        if (
            data.result === "incomplete"
        ) {

            showMessage(
                "⚠️ Fill in all the empty cells first.",
                "warning"
            );

            return;
        }

        // ====================================================
        // CORRECT SOLUTION
        // ====================================================

        if (
            data.result === "correct"
        ) {

            // Stop the timer first.
            stopTimer();

            // Get final solving time in seconds.
            const solvingTime =
                Math.floor(
                    (Date.now() - startTime) / 1000
                );

            // ====================================================
            // SAVE SCORE TO DATABASE
            // ====================================================

            const scoreResponse =
                await fetch("/api/save-score", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        player_id:
                            playerId,

                        puzzle_size:
                            puzzleSize,

                        solving_time:
                            solvingTime
                    })

                });

            const scoreData =
                await scoreResponse.json();

            if (!scoreResponse.ok) {

                throw new Error(
                    scoreData.error ||
                    "Unable to save score."
                );
            }

            // ====================================================
            // UPDATE BEST TIME ON SCREEN
            // ====================================================

            bestTimeElement.textContent =
                formatTime(
                    scoreData.best_time
                );

            // ====================================================
            // DISPLAY RESULT
            // ====================================================

            if (
                scoreData.new_best
            ) {

                showMessage(
                    `🎉 Congratulations, ${username}!<br><br>
                     🏆 New Best Time: <strong>${formatTime(solvingTime)}</strong>`,
                    "success"
                );

            }
            else {

                showMessage(
                    `🎉 Congratulations, ${username}!<br><br>
                     ⏱️ Your Time: <strong>${formatTime(solvingTime)}</strong><br>
                     🏆 Best Time: <strong>${formatTime(scoreData.best_time)}</strong>`,
                    "success"
                );
            }

            return;
        }

        // ====================================================
        // INCORRECT SOLUTION
        // ====================================================

        showMessage(
            `❌ ${data.message}`,
            "error"
        );

    }

    catch (error) {

        console.error(
            "Check/save score error:",
            error
        );

        showMessage(
            error.message ||
            "Unable to check or save the answer.",
            "error"
        );
    }
}


// ============================================================
// RESET
// ============================================================

resetButton.addEventListener(
    "click",
    resetPuzzle
);


function resetPuzzle() {

    if (!originalBoard) {

        return;
    }


    board =
        originalBoard.map(
            row => [...row]
        );


    selectedCell = null;


    renderBoard();


    hideMessage();


    startTimer();
}


// ============================================================
// TIMER
// ============================================================

function startTimer() {

    stopTimer();


    startTime =
        Date.now();


    timerElement.textContent =
        "00:00";


    timerInterval =
        setInterval(
            updateTimer,
            1000
        );
}


function updateTimer() {

    if (!startTime) {

        return;
    }


    const elapsed =
        Math.floor(
            (Date.now() - startTime) / 1000
        );


    timerElement.textContent =
        formatTime(elapsed);
}


function stopTimer() {

    if (timerInterval) {

        clearInterval(
            timerInterval
        );


        timerInterval = null;
    }
}


function getElapsedTime() {

    if (!startTime) {

        return "00:00";
    }


    const elapsed =
        Math.floor(
            (Date.now() - startTime) / 1000
        );


    return formatTime(
        elapsed
    );
}


function formatTime(totalSeconds) {

    const minutes =
        Math.floor(
            totalSeconds / 60
        );


    const seconds =
        totalSeconds % 60;


    return (

        String(minutes).padStart(
            2,
            "0"
        )

        +

        ":"

        +

        String(seconds).padStart(
            2,
            "0"
        )

    );
}


// ============================================================
// UI MESSAGES
// ============================================================

function showMessage(
    message,
    type
) {

    messageElement.innerHTML =
        message;


    messageElement.className =
        `message ${type}`;
}


function hideMessage() {

    messageElement.className =
        "message hidden";


    messageElement.innerHTML =
        "";
}


// ============================================================
// CLEAR BOARD
// ============================================================

function clearBoard() {

    board = null;

    originalBoard = null;

    selectedCell = null;

    boardElement.innerHTML = "";

    numberPad.innerHTML = "";

    hideMessage();
}