from .piece import Piece


class King(Piece):

    def __init__(self, row, col, color, image):
        super().__init__(row, col, color, image)

    def find_legal_moves(self, board):
        legal_moves = {}
        row = self.row
        col = self.col
        return legal_moves
