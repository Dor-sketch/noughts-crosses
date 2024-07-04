"""
This module contains the GameBoard class which is responsible for rendering the
game board and handling user input.
The GameBoard is a composition of the NoughtsCrosses game, the ScoreKeeper,
the BoardRenderer, the ScoreRenderer, and the EventHandler.
"""

import pygame
import asyncio
from noughts_crosses import NoughtsCrosses
from event_handler import EventHandler
from renderer import BoardRenderer, ScoreRenderer
from score_keeper import ScoreKeeper


GRID_SIZE = 200  # Size of each grid cell
BOARD_SIZE = (GRID_SIZE * 3, GRID_SIZE * 3)  # Size of the game board


class GameBoard:
    """
    The GameBoard class is responsible for rendering the game board and handling user input.
    """

    def __init__(self, game, board_size=BOARD_SIZE):
        pygame.font.init()
        self.game = game
        self.board_size = board_size
        self.screen_size = (self.board_size[0] + GRID_SIZE, self.board_size[1])
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Noughts and Crosses")
        self.font_size = GRID_SIZE
        self.reset_button = pygame.Rect(
            self.board_size[0] + GRID_SIZE // 2,
            GRID_SIZE // 2,
            GRID_SIZE // 2,
            GRID_SIZE // 4,
        )
        self.board_renderer = BoardRenderer(self.screen, self.board_size, GRID_SIZE)
        self.score_renderer = ScoreRenderer(
            self.screen, self.board_size, self.font_size, GRID_SIZE)
        self.score_keeper = ScoreKeeper()
        self.event_handler = EventHandler(
            self.game, self.board_renderer, self.reset_button, GRID_SIZE
        )

    async def run(self):
        """
        Run the game.
        """
        running = True
        dirty = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.event_handler.handle_event(event)
                        dirty = True
                if dirty:
                    dirty = False
                    await self.board_renderer.draw_board(self.game)
                    winner = self.game.check_winner()

                    if winner:
                        if winner != "Tie":
                            self.score_keeper.increment_score(winner)
                            play_again = await self.board_renderer.draw_winner(
                                winner, self.game)
                            if play_again:
                                self.game.reset()
                                await self.board_renderer.draw_board(self.game)
                            else:
                                running = False
                        else:
                            await self.score_renderer.draw_reset_button(reset_button=self.reset_button)
                    await self.score_renderer.draw_score_board(
                        self.score_keeper
                    )
                    pygame.display.flip()
            except Exception as e:
                print(f"An error occurred: {e}")
            await asyncio.sleep(0)  # Very important, and keep it 0
        pygame.quit()


async def main():
    """
    Entry point for the game.
    """
    game = NoughtsCrosses()
    gui = GameBoard(game)
    await gui.run()

if __name__ == '__main__':
    asyncio.run(main())
