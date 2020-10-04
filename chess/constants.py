import pygame

HEIGHT = 800
WIDTH = 1200
SQUARE_SIZE = 100
BLACK_BISHOP = pygame.image.load("resources/bb.png")
WHITE_BISHOP = pygame.image.load("resources/wb.png")
BLACK_ROOK = pygame.image.load("resources/br.png")
WHITE_ROOK = pygame.image.load("resources/wr.png")
BLACK_KING = pygame.image.load("resources/bk.png")
WHITE_KING = pygame.image.load("resources/wk.png")
BLACK_KNIGHT = pygame.image.load("resources/bn.png")
WHITE_KNIGHT = pygame.image.load("resources/wn.png")
BLACK_QUEEN = pygame.image.load("resources/bq.png")
WHITE_QUEEN = pygame.image.load("resources/wq.png")
BLACK_PAWN = pygame.image.load("resources/bp.png")
WHITE_PAWN = pygame.image.load("resources/wp.png")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_SQUARE = (0, 153, 51)
LIGHT_BLUE = (135, 206, 250)
RED = (255, 0, 0)
ROWS = COLS = 8
POSSIBLE_MOVE_RADIUS = 15
BOARD_EDGE = 25
TEXT_OFFSET = 10
FPS = 60
