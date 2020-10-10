import pygame
from chess.constants import ENGINE_STRENGTH
from gameflow.gameflow import GameFlow


def main():
    pygame.init()
    game_flow = GameFlow(ENGINE_STRENGTH)
    game_flow.play()


if __name__ == "__main__":
    main()
