"""
This module contains the classes for rendering the game board and the score board
"""

import pygame
from pygame.locals import *
import asyncio
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Renderer:
    def __init__(self, screen, board_size, grid_size):
        self._screen = screen
        self._board_size = board_size
        # init font
        pygame.font.init()
        self._font_size = 30
        self._grid_size = grid_size

    def get_screen(self):
        return self._screen

    def get_board_size(self):
        return self._board_size

    def get_font_size(self):
        return self._font_size

    def get_grid_size(self):
        return self._grid_size

class BoardRenderer(Renderer):
    def __init__(self, screen, board_size, grid_size):
        super().__init__(screen, board_size, grid_size)
        self._board_lines = [
            ((self._grid_size, 0), (self._grid_size, self._board_size[1])),
            ((self._grid_size * 2, 0),
             (self._grid_size * 2, self._board_size[1])),
            ((0, self._grid_size), (self._board_size[0], self._grid_size)),
            ((0, self._grid_size * 2),
             (self._board_size[0], self._grid_size * 2)),
        ]
        self.gradient_surface = self.get_gradient_surface()
        try:
            self._x_img = pygame.image.load('images/x_image.svg')
            self._o_img = pygame.image.load('images/o_image.svg')
            self._o_img = pygame.transform.scale(
                self._o_img, (self._grid_size * 4 // 5, self._grid_size * 4 // 5))
            self._x_img = pygame.transform.scale(
                self._x_img, (self._grid_size * 4 // 5, self._grid_size * 4 // 5))
        except FileNotFoundError:
            # Create surfaces for X and O with transparent background
            self._x_img = pygame.Surface((self._grid_size * 4 // 5, self._grid_size * 4 // 5), pygame.SRCALPHA)
            self._o_img = pygame.Surface((self._grid_size * 4 // 5, self._grid_size * 4 // 5), pygame.SRCALPHA)

            # Set color for X and O
            color = (0, 0, 0)  # Black color

            # Draw X on the surface
            pygame.draw.line(self._x_img, color, (0, 0), (self._x_img.get_width(), self._x_img.get_height()), 5)
            pygame.draw.line(self._x_img, color, (0, self._x_img.get_height()), (self._x_img.get_width(), 0), 5)

            # Draw O on the surface
            pygame.draw.ellipse(self._o_img, color, self._o_img.get_rect(), 5)

            # Save the images
            pygame.image.save(self._x_img, 'x_img.png')
            pygame.image.save(self._o_img, 'o_img.png')

            # Load the images
            self._x_img = pygame.image.load('x_img.png').convert_alpha()
            self._o_img = pygame.image.load('o_img.png').convert_alpha()

        self._small_font = pygame.font.Font(None, 25)

    def get_gradient_surface(self):
        if os.path.exists('images/gradient_surface.png'):
            return pygame.image.load('images/gradient_surface.png')
        gradient_surface = pygame.Surface(self.get_screen().get_size())
        height = gradient_surface.get_height()
        for y in range(height):
            color = (min((y * 255) // height, 255), min((y * 255) // (height // 2), 255), min((y * 255) // (height // 3), 255))
            pygame.draw.line(gradient_surface, color, (0, y), (gradient_surface.get_width(), y))
        # save as image
        pygame.image.save(gradient_surface, 'images/gradient_surface.png')
        return gradient_surface

    def get_grid_size(self):
        return self._grid_size

    async def draw_board(self, game):
        screen = self.get_screen()
        screen.blit(self.gradient_surface, (0, 0))

        for line in self._board_lines:
            pygame.draw.line(screen, BLACK, line[0], line[1], 5)

        for i, cell in enumerate(game.get_board()):
            x = (i % 3) * self._grid_size + self._grid_size // 10
            y = (i // 3) * self._grid_size + self._grid_size // 10
            if cell == 'X':
                screen.blit(self._x_img, (x, y))
            elif cell == 'O':
                screen.blit(self._o_img, (x, y))

    async def animate_winning_line(self, combo):
        """
        Animate a line through the winning combination
        """
        screen = self.get_screen()
        GRID_SIZE = self.get_grid_size()
        winning_line = [
            ((combo[0] % 3) * GRID_SIZE + GRID_SIZE // 2,
             (combo[0] // 3) * GRID_SIZE + GRID_SIZE // 2),
            ((combo[2] % 3) * GRID_SIZE + GRID_SIZE // 2,
             (combo[2] // 3) * GRID_SIZE + GRID_SIZE // 2),
        ]

        dx = winning_line[1][0] - winning_line[0][0]
        dy = winning_line[1][1] - winning_line[0][1]
        steps = max(abs(dx), abs(dy))

        for i in range(steps + 1):
            x = winning_line[0][0] + i * dx // steps
            y = winning_line[0][1] + i * dy // steps
            pygame.draw.line(screen, RED, winning_line[0], (x, y), 5)
            pygame.display.flip()

    async def draw_winning_line(self, combo, winner):
        """
        Draw a line through the winning combination
        """
        GRID_SIZE = self.get_grid_size()
        screen = self.get_screen()
        winning_line = [
            ((combo[0] % 3) * GRID_SIZE + GRID_SIZE // 2,
             (combo[0] // 3) * GRID_SIZE + GRID_SIZE // 2),
            ((combo[2] % 3) * GRID_SIZE + GRID_SIZE // 2,
             (combo[2] // 3) * GRID_SIZE + GRID_SIZE // 2),
        ]

        pygame.draw.line(screen, RED, winning_line[0], winning_line[1], 5)
        text = self._small_font.render(f'{str(winner)} wins!', True, RED)
        text_rect = text.get_rect(center=(self.get_board_size()[0] + 80, self.get_board_size()[1] // 2))
        screen.blit(text, text_rect)

        pygame.display.flip()
        await asyncio.sleep(1)

    async def draw_winner(self, winner, game):
        """
        Draw the winner text on the screen
        """
        if winner == 'Tie':
            text = 'It\'s a Tie!'
        else:
            text = f'{winner} wins!'
        await self.draw_winning_line(game.winning_combo, winner)
        return True


    async def draw_play_again_button(self):
        """
        Draw the play again button on the screen
        """
        screen = self.get_screen()
        board_size = self.get_board_size()
        # Position the play button below the winner text
        play_button = pygame.Rect(
            board_size[0] // 2 - 100, board_size[1] // 2 + 50, 100, 50)
        # Position the quit button next to the play button
        quit_button = pygame.Rect(
            board_size[0] // 2, board_size[1] // 2 + 50, 100, 50)
        pygame.draw.rect(screen, BLACK, play_button)  # Draw the play button
        pygame.draw.rect(screen, BLACK, quit_button)  # Draw the quit button
        play_text = self._small_font.render('Play again?', True, WHITE)
        quit_text = self._small_font.render('Quit', True, WHITE)
        play_text_rect = play_text.get_rect(center=play_button.center)
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(play_text, play_text_rect)
        screen.blit(quit_text, quit_text_rect)

        while True:  # Wait for the user to click a button
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif quit_button.collidepoint(pygame.mouse.get_pos()):
                        return False
            pygame.display.flip()


class ScoreRenderer(Renderer):
    def __init__(self, screen, board_size, font_size, grid_size):
        super().__init__(screen, board_size, grid_size)
        self._font_size = font_size
        self._font = pygame.font.Font(None, self._font_size)
        self._small_font = pygame.font.Font(None, self._font_size // 5)
        self.gradient_surface = self.get_score_gradient_surface()


    def get_score_gradient_surface(self):
        GRID_SIZE = self._grid_size
        if os.path.exists('images/score_gradient_surface.png'):
            return pygame.image.load('images/score_gradient_surface.png')
        gradient_surface = pygame.Surface(
            (self.get_board_size()[0] + GRID_SIZE, GRID_SIZE // 2))
        width = gradient_surface.get_width()
        for x in range(width):
            color = (min((x * 255) // width, 255), min((255 - (x * 255) // width), 255), 150)
            pygame.draw.line(gradient_surface, color, (x, 0),
                             (x, gradient_surface.get_height()))
        gradient_surface = pygame.transform.flip(gradient_surface, False, True)
        # save as image
        pygame.image.save(gradient_surface, 'images/score_gradient_surface.png')
        return gradient_surface

    async def draw_score_board(self, score_keeper):
        GRID_SIZE = self.get_grid_size()
        board_size = self.get_board_size()
        screen = self.get_screen()
        x_wins, o_wins = score_keeper.get_scores()
        text = self._small_font.render(
            f'X: {x_wins} | O: {o_wins}', True, BLACK)
        text_rect = text.get_rect()
        text_rect.topleft = (board_size[0] + GRID_SIZE // 10, GRID_SIZE // 10)

        screen.blit(self.gradient_surface,
                    (text_rect.left - 10, text_rect.top - 10))
        screen.blit(text, text_rect)

    async def draw_reset_button(self, reset_button):
        screen = self.get_screen()
        pygame.draw.rect(screen, BLACK, reset_button.inflate(-20, -10))
        text = self._small_font.render('Reset', True, WHITE)
        text_rect = text.get_rect(center=reset_button.center)
        screen.blit(text, text_rect)
