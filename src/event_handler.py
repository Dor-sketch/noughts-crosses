"""
This module contains the EventHandler class which is responsible for handling the events in the game.
"""

import pygame


class EventHandler:
    """
    The EventHandler class is responsible for handling the events in the game.
    """
    def __init__(self, game, board_renderer, reset_button, GRID_SIZE):
        self.game = game
        self.board_renderer = board_renderer
        self.reset_button = reset_button
        self.GRID_SIZE = GRID_SIZE

    def handle_event(self, event):
        """
        Handle the events in the game.
        """
        GRID_SIZE = self.GRID_SIZE
        board_size = self.board_renderer.get_board_size()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.reset_button.collidepoint(pygame.mouse.get_pos()):
                self.reset_game()
            else:
                x, y = pygame.mouse.get_pos()
                if x < board_size[0] and y < board_size[1]:
                    position = (y // GRID_SIZE) * 3 + (x // GRID_SIZE)
                    self.game.make_move(position)

    def reset_game(self):
        """
        Reset the game.
        """
        self.game.reset()
