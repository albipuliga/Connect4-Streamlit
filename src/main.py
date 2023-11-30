from utils import *


def main():
    game = ConnectFour()
    game_over = False

    while not game_over:
        game.print_board()
        if game.turn == "X":
            try:
                column = int(input("Player X, choose a column (0-6): "))
                if not game.insert_disc(column, "X"):
                    print("Column full or invalid. Try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
        else:
            print("AI is making a move...")
            ai_column = game.greedy_move()
            game.insert_disc(ai_column, "O")
            print(f"AI chose column {ai_column}")

        if game.check_winner(game.turn):
            game.print_board()
            print(f"Player {game.turn} wins!")
            break

        if game.is_full():
            game.print_board()
            print("The game is a draw.")
            break

        game.turn = "O" if game.turn == "X" else "X"


if __name__ == "__main__":
    main()
