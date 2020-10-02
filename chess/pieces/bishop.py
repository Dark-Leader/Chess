from .piece import Piece
from chess.constants import WHITE


class Bishop(Piece):

    def __init__(self, row, col, color, image):
        super().__init__(row, col, color, image)

    def find_legal_moves(self, board):
        legal_moves = {}
        legal_moves.update(self.find_top_left_diagonal_moves(board))
        legal_moves.update(self.find_top_right_diagonal_moves(board))
        legal_moves.update(self.find_bottom_left_diagonal_moves(board))
        legal_moves.update(self.find_bottom_right_diagonal_moves(board))
        return legal_moves

    def to_fen(self):
        if self.color == WHITE:
            return "B"
        else:
            return "b"
