import pygame
from chess.constants import WIDTH, HEIGHT, FPS, BOARD_EDGE
from chess.game import Game
# from chess.engine import Engine
pygame.init()
window = pygame.display.set_mode((WIDTH + BOARD_EDGE * 2, HEIGHT + BOARD_EDGE * 2))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
game = Game(window)
# engine = Engine()
# engine.get_response()
# engine.put_command("uci")
# engine.get_response()
# engine.put_command('quit')

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            game.select(pos)

    game.update()
    result = game.get_winner()
    if result:
        print(result)
        running = False
    pygame.display.flip()

pygame.quit()
