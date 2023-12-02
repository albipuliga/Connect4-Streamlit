import pandas as pd
import streamlit as st

from utils import ConnectFour

if "users_df" not in st.session_state:
    st.session_state.users_df = pd.DataFrame(
        columns=["Username", "Wins", "Losses", "Win/Loss Ratio"]
    )


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
                            f'<div style="width: 50px; height: 50px; '
                            f'background-color: green; border-radius: 50%; margin: 10px;"></div>',
                            unsafe_allow_html=True,
                        )
                    elif (
                            st.session_state.game.board[acc_row][acc_col] == "O"
                    ):  # machine
                        st.markdown(
                            f'<div style="width: 50px; height: 50px; '
                            f'background-color: red; border-radius: 50%; margin: 10px;"></div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div style="width: 50px; height: 50px; '
                            f'background-color: grey; border-radius: 50%; margin: 10px;"></div>',
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


def main_loop():
    st.title("Connect 4")
    columns = 7
    rows = 6

    # Initialize the game board and game_over flag
    if "game" not in st.session_state:
        st.session_state.game = ConnectFour()
        st.session_state.game_over = False

    # Player usernames
    username = st.text_input("Enter username:")
    if username == "":
        st.warning("Please enter a username.")
        st.stop()

    # # Ensure the username is unique
    # if username in st.session_state.users_df["Username"].values:
    #     st.error("Username already exists. Please choose a different one.")
    #     st.stop()

    # Check if the user already exists in the DataFrame
    if username not in st.session_state.users_df["Username"].values:
        # Add a new row for the user
        new_user_row = pd.DataFrame(
            [[username, 0, 0, 0]],
            columns=["Username", "Wins", "Losses", "Win/Loss Ratio"],
        )
        st.session_state.users_df = pd.concat(
            [st.session_state.users_df, new_user_row], ignore_index=True
        )
        st.session_state.users_df = st.session_state.users_df.sort_values(
            by="Win/Loss Ratio", ascending=False
        )

    # Choose who starts
    st.session_state.selected_option = st.selectbox("Who starts?", ["Machine", "User"])

    # Reset the game
    if st.button("Reset"):
        st.session_state.game = ConnectFour()
        if st.session_state.selected_option == "Machine":
            st.session_state.game_over = False
            machine_moves(st.session_state.game)

    # Player input
    col = st.number_input("Choose a column (0-6):", 0, columns - 1, format="%d")

    response_container = st.container()
    with response_container:
        if st.button("Drop Chip"):
            if st.session_state.game_over:
                st.warning("Game over. Please reset the game to play again.")
            elif is_col_full(st.session_state.game.board, col):
                st.error("Column is full!")
            else:
                player_moves(st.session_state.game, col)
                user_index = st.session_state.users_df[
                    st.session_state.users_df["Username"] == username
                    ].index[0]
                # Check if player won
                if st.session_state.game.check_winner("X"):
                    draw(columns, rows)
                    st.success(f"{username} won!")
                    st.session_state.users_df.at[user_index, "Wins"] += 1
                    st.session_state.game_over = True
                    return username

                if not st.session_state.game_over:
                    machine_moves(st.session_state.game)
                    # Check if machine won
                    if st.session_state.game.check_winner("O"):
                        st.error("You lost!")
                        st.session_state.users_df.at[user_index, "Losses"] += 1
                        draw(columns, rows)
                        st.session_state.game_over = True
                        return None

                st.session_state.users_df.at[user_index, "Win/Loss Ratio"] = (
                    st.session_state.users_df.at[user_index, "Wins"]
                    / st.session_state.users_df.at[user_index, "Losses"]
                    if st.session_state.users_df.at[user_index, "Losses"] > 0
                    else float("inf")
                )

        draw(columns, rows)


main_loop()
