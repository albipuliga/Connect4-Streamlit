# Connect4 Game

This is a simple implementation of the classic Connect4 game using Python and Streamlit.

## Project Structure

- `src/play.py`: This is the main script that runs the game. It handles user input, game logic, and rendering the game board.
- `src/utils.py`: This file contains the `ConnectFour` class, which represents the game board and includes methods for inserting discs, checking for a winner, and making a move.
- `.gitignore`: This file specifies the directories and files that should be ignored by Git.

## How to Run

1. Ensure you have Python and Streamlit installed on your machine.
2. Navigate to the project directory.
3. Run the command `streamlit run src/play.py` to start the game.

## Game Rules

1. Players take turns dropping one disc into any of the seven columns.
2. The disc can fall into the lowest empty space within the selected column.
3. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four discs.

Enjoy the game!