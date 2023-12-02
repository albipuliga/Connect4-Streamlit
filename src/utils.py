class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.board = [[" " for _ in range(self.columns)] for _ in range(self.rows)]
        self.turn = "X"  # X will start

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