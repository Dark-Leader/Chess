from chess.game import Game
from chess.constants import WHITE, WIDTH, HEIGHT, BOARD_EDGE, FPS
import pygame


class GameFlow:

    def __init__(self, skill_level):
        self.window = pygame.display.set_mode((WIDTH + 2 * BOARD_EDGE, HEIGHT + 2 * BOARD_EDGE))
        pygame.display.set_caption("Chess")
        self.clock = pygame.time.Clock()
        self.game = Game(self.window, skill_level)
        self.game_over = False

    def update_display(self):
        self.game.update()

    def make_player_move(self, position):
        self.game.select(position)

    def make_engine_move(self):
        self.game.make_engine_move()

    def play(self):
        while not self.game_over:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if self.game.turn == WHITE:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        self.game.select(pos)
                else:
                    self.game.make_engine_move()
            self.update_display()
            result = self.game.get_winner()
            if result:
                print(result)
                self.game.reset()
                # self.game_over = True
            pygame.display.flip()

        pygame.quit()




