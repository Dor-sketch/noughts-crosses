"""
This module contains the ScoreKeeper class which is responsible for keeping
track of the scores of the game.
"""

class ScoreKeeper:
    def __init__(self, max_score=999):
        self.x_wins = 0
        self.o_wins = 0
        self.max_score = max_score

    def increment_score(self, player):
        if player == 'X':
            self.x_wins += 1
        elif player == 'O':
            self.o_wins += 1

    def get_scores(self):
        return self.x_wins, self.o_wins