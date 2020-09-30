from chess.board import Board
from chess.constants import WHITE, BLACK, LIGHT_BLUE, SQUARE_SIZE, POSSIBLE_MOVE_RADIUS
import pygame


class Game:

    def __init__(self, win):
        self.win = win
        self._initialize()

    def _initialize(self):
        self.board = Board()
        self.selected = None
        self.turn = WHITE
        self.valid_moves = {}
        self.winner = None

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves()

    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.win, LIGHT_BLUE, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                                      int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), POSSIBLE_MOVE_RADIUS)

    def select(self, position):
        row, col = self.get_position(position)
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(position)
                self.valid_moves = {}
        piece = self.board.get_piece(row, col)
        if piece is not None and piece.get_color() == self.turn:
            self.selected = piece
            self.valid_moves = self.board.find_legal_moves(piece)
            return True
        return False

    @staticmethod
    def get_position(position):
        x, y = position
        row = int(y // SQUARE_SIZE)
        col = int(x // SQUARE_SIZE)
        return row, col

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col, self.board.board)
            capture = self.valid_moves[(row, col)]
            if capture:
                capture_row, capture_col = capture
                if capture_row != row:  # en passant
                    self.board.remove(self.board.board, capture)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        self.board.stop_en_passant(self.turn)
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        self.board.find_all_possible_moves(self.turn)
        self.winner = self.board.checkmate_or_stalemate(self.turn)

    def reset(self):
        self._initialize()

    def get_winner(self):
        return self.winner

