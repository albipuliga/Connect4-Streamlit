# utils.py
import random

class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = [[" " for _ in range(self.columns)] for _ in range(self.rows)]
        self.turn = "X"  # X will start
        self.depth = 3  # Depth for the minimax algorithm

    def insert_disc(self, column, player):
        if self.board[0][column] != " ":
            return False  # Column is full

        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == " ":
                self.board[row][column] = player
                return True
        return False

    def check_winner(self, player):
        # Check horizontal, vertical, and diagonal for a win
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row][c] == player for c in range(col, col + 4)):
                    return True

        for col in range(self.columns):
            for row in range(self.rows - 3):
                if all(self.board[r][col] == player for r in range(row, row + 4)):
                    return True

        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False

    def greedy_move(self):
        for col in range(self.columns):
            if self.simulate_move(col, "O"):
                return col

        for col in range(self.columns):
            if self.simulate_move(col, "X"):
                return col

        # Fallback strategy: choose the center or the closest available column
        for offset in range(self.columns // 2 + 1):
            for col in [self.columns // 2 + offset, self.columns // 2 - offset]:
                if 0 <= col < self.columns and self.board[0][col] == " ":
                    return col

    def minimax_move(self):
        best_score = float('-inf')
        best_move = None

        for col in range(self.columns):
            if not self.is_col_full(col):
                row = self.get_next_open_row(col)
                self.insert_disc(col, "O")
                score = self.minimax(self.depth, False)
                self.board[row][col] = " "  # Undo the move

                if score > best_score:
                    best_score = score
                    best_move = col

        return best_move

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.check_winner("O") or self.check_winner("X") or self.is_board_full():
            return self.evaluate_board(self.board)

        if maximizing_player:
            max_eval = float("-inf")
            for col in range(self.columns):
                if not self.is_col_full(col):
                    row = self.get_next_open_row(col)
                    self.insert_disc(col, "O")
                    eval = self.minimax(depth - 1, False)
                    self.board[row][col] = " "  # Undo the move
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for col in range(self.columns):
                if not self.is_col_full(col):
                    row = self.get_next_open_row(col)
                    self.insert_disc(col, "X")
                    eval = self.minimax(depth - 1, True)
                    self.board[row][col] = " "  # Undo the move
                    min_eval = min(min_eval, eval)
            return min_eval

    def get_next_open_row(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == " ":
                return row

    def is_col_full(self, col):
        return self.board[0][col] != " "

    def is_board_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def evaluate_board(self, board):
        # Check for a win
        if self.check_winner("O"):
            return 10  # "O" wins, maximizing player
        elif self.check_winner("X"):
            return -10  # "X" wins, minimizing player

        # Count the number of open two-in-a-row, three-in-a-row, and four-in-a-row for each player
        score = 0

        # Check rows
        for row in range(self.rows):
            for col in range(self.columns - 3):
                score += self.score_position(board[row][col:col + 4])

        # Check columns
        for col in range(self.columns):
            for row in range(self.rows - 3):
                score += self.score_position([board[row + i][col] for i in range(4)])

        # Check diagonals
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                score += self.score_position([board[row + i][col + i] for i in range(4)])

        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                score += self.score_position([board[row - i][col + i] for i in range(4)])

        return score

    def score_position(self, position):
        # Assign scores based on the number of "O" and "X" in a position
        o_count = position.count("O")
        x_count = position.count("X")

        if o_count == 4:
            return 100
        elif o_count == 3 and x_count == 0:
            return 5
        elif o_count == 2 and x_count == 0:
            return 2
        elif x_count == 4:
            return -100
        elif x_count == 3 and o_count == 0:
            return -5
        elif x_count == 2 and o_count == 0:
            return -2

        return 0

    def simulate_move(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == " ":
                self.board[row][col] = player
                win = self.check_winner(player)
                self.board[row][col] = " "  # Undo the move
                if win:
                    return True
                break
        return False
