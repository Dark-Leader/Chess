import pygame
from chess.constants import WIDTH, HEIGHT, FPS, BOARD_EDGE, WHITE
from chess.game import Game
import time
# from chess.engine import Engine
pygame.init()
window = pygame.display.set_mode((WIDTH + BOARD_EDGE * 2, HEIGHT + BOARD_EDGE * 2))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
game = Game(window)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game.turn == WHITE:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            game.select(pos)

    else:
        game.make_engine_move()
        time.sleep(1)

    game.update()
    result = game.get_winner()
    if result:
        print(result)
        running = False
    pygame.display.flip()

pygame.quit()


# engine = Engine()
# engine.set_position("rnbqk3/ppppp2P/8/8/8/8/PPPPPPP1/RNBQKBNR w KQq - 0 1")
# print(engine.get_move(500))