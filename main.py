import pygame
from chess.constants import WIDTH, HEIGHT, FPS
from chess.game import Game
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
game = Game(window)

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
    pygame.display.flip()

pygame.quit()