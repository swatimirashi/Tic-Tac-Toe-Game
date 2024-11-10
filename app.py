from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Initialize global variables to maintain the state across games
board = [""] * 9  # Represents the 9 cells of the Tic-Tac-Toe board, initially empty
turn = "X"  # Default starting player
winner = None  # No winner initially
previous_winner = None  # Tracks the winner of the previous game

@app.route("/", methods=["GET", "POST"])
def index():
    global board, turn, winner, previous_winner
    
    # Reset game state for a new game on a GET request (e.g., page load)
    if request.method == "GET":
        # Set starting player based on the previous game’s winner
        if previous_winner == "X":
            turn = "X"  # X won last game, so X starts
        elif previous_winner == "O":
            turn = "O"  # O won last game, so O starts
        else:
            turn = "X"  # No previous winner (first game), X starts by default
        
        # Reset board and winner status for a fresh game
        board = [""] * 9
        winner = None

    # Handle player's move on a POST request (form submission)
    elif request.method == "POST":
        index = int(request.form["index"])  # Get the cell index from the form

        # Only proceed if the selected cell is empty and there is no winner yet
        if board[index] == "" and winner is None:
            board[index] = turn  # Mark the board with the current player's symbol

            # Check if this move results in a win
            if check_winner():
                winner = turn  # Set the winner to the current player
                previous_winner = turn  # Update the previous winner for the next game
            elif "" not in board:
                winner = "Draw"  # If the board is full and no winner, it’s a draw
                # Do not update previous_winner on a draw, so it keeps the last winner
            else:
                # No win or draw, so switch turns to the other player
               if turn == "X":
                   turn = "O"
               else:
                   turn = "X"

                    
    # Render the game board with the current board state, winner, and turn info
    return render_template("index.html", board=board, winner=winner, turn=turn)

@app.route("/reset", methods=["POST"])
def reset():
    """
    Resets the game state to start a new game, used by the reset button.
    This resets the board and winner, and sets turn to 'X' as default.
    """
    global board, turn, winner
    board = [""] * 9  # Reset the board to all empty cells
    turn = "X"  # Default turn to X when reset manually
    winner = None  # Clear any winner
    return redirect(url_for('index'))  # Redirect to the main page

def check_winner():
    """
    Check the board to determine if there is a winning combination.
    Returns True if a winning combination is found; otherwise, returns False.
    """
    # Check rows for a win
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] != "":
            return True
    
    # Check columns for a win
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != "":
            return True

    # Check diagonals for a win
    if board[0] == board[4] == board[8] != "" or board[2] == board[4] == board[6] != "":
        return True

    return False  # No winning combination found

if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask application in debug mode
