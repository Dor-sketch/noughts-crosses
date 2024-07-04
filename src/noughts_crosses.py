"""
Game logic for the Noughts and Crosses Game
"""


class NoughtsCrosses:
    """
    The NoughtsCrosses class is responsible for the game logic.
    """
    def __init__(self):
        self.board = [' ']*9
        self.current_player = 'X'
        self.winning_combo = None

    def make_move(self, position):
        """
        Make a move in the game.
        """
        if position < 0 or position > 8:
            raise ValueError('Position must be between 0 and 8')

        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.winning_combo = combo
                return self.board[combo[0]]

        if ' ' not in self.board:
            return 'Tie'

        return None

    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def reset(self):
        self.board = [' ']*9
        self.current_player = 'X'
        self.winning_combo = None

    def __str__(self):
        board = self.board
        return f'{board[0]}|{board[1]}|{board[2]}\n-----\n{board[3]}|{board[4]}|{board[5]}\n-----\n{board[6]}|{board[7]}|{board[8]}'
