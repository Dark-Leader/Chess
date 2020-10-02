from .piece import Piece
from chess.constants import WHITE


class Rook(Piece):

    def __init__(self, row, col, color, image):
        super().__init__(row, col, color, image)
        self.moved_before = False

    def find_legal_moves(self, board):
        legal_moves = {}
        legal_moves.update(self.find_top_moves(board))
        legal_moves.update(self.find_bottom_moves(board))
        legal_moves.update(self.find_right_moves(board))
        legal_moves.update(self.find_left_moves(board))
        return legal_moves

    def move(self, row, col):
        super().move(row, col)
        self.moved_before = True

    def to_fen(self):
        if self.color == WHITE:
            return "R"
        else:
            return "r"
