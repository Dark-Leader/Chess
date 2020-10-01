import pygame
from chess.constants import BLACK


class Button:

    def __init__(self, x, y, width, height, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.name = name

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, 1, BLACK)
        win.blit(text, ((self.x * 2 + self.width) // 2, (self.y * 2 + self.height) // 2))

    def clicked(self, position):
        x, y = position
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
