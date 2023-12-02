import numpy as np
import streamlit as st

from utils import ConnectFour


# Function to draw the board
def draw(num_columns, num_rows):
    st.title("Board")
    columns = st.columns(num_columns)
    acc_col = -1
    acc_row = -1
    while acc_col < 6:
        for col in columns:
            if acc_row > 4:
                acc_row = -1

            acc_col += 1
            with col:
                for circle in range(num_rows):
                    acc_row += 1
                    if st.session_state.game.board[acc_row][acc_col] == "X":  # player
                        st.markdown(
                            f'<div style="width: 50px; height: 50px; background-color: green; border-radius: 50%; margin: 10px;"></div>',
                            unsafe_allow_html=True,
                        )
                    elif (
                        st.session_state.game.board[acc_row][acc_col] == "O"
                    ):  # machine
                        st.markdown(
                            f'<div style="width: 50px; height: 50px; background-color: red; border-radius: 50%; margin: 10px;"></div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div style="width: 50px; height: 50px; background-color: grey; border-radius: 50%; margin: 10px;"></div>',
                            unsafe_allow_html=True,
                        )


# Function for machine moves
def machine_moves(game, player="O"):
    col = game.greedy_move()
    game.insert_disc(col, player)


# Function to check if a column is full
def is_col_full(board, col):
    return board[0][col] != " "


# Function to process player moves
def player_moves(game, col, player="X"):
    if not is_col_full(game.board, col):
        game.insert_disc(col, player)


st.title("Connect 4")
num_columns = 7
num_rows = 6


# Initialize the game board and game_over flag
if "game" not in st.session_state:
    st.session_state.game = ConnectFour()
    st.session_state.game_over = False

# Player usernames
player1_username = st.text_input("Enter username:")

# Choose who starts
st.session_state.selected_option = st.selectbox("Who starts?", ["Machine", "User"])


# Reset the game
if st.button("Reset"):
    st.session_state.game = ConnectFour()
    if st.session_state.selected_option == "Machine":
        st.session_state.game_over = False
        machine_moves(st.session_state.game)

# Player input
col = st.number_input("Choose a column (0-6):", 0, num_columns - 1, format="%d")

response_container = st.container()
with response_container:
    if st.button("Drop Chip"):
        if st.session_state.game_over:
            st.warning("Game over. Please reset the game to play again.")
        elif is_col_full(st.session_state.game.board, col):
            st.error("Column is full!")
        else:
            player_moves(st.session_state.game, col)
            # Check if player won
            if st.session_state.game.check_winner("X"):
                draw(num_columns, num_rows)
                st.success(f"{player1_username} won!")
                st.session_state.game_over = True
                st.stop()

            if not st.session_state.game_over:
                machine_moves(st.session_state.game)
                # Check if machine won
                if st.session_state.game.check_winner("O"):
                    st.error("You lost!")
                    draw(num_columns, num_rows)
                    st.session_state.game_over = True
                    st.stop()

    draw(num_columns, num_rows)
