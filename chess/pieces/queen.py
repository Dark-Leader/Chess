from .piece import Piece


class Queen(Piece):

    def __init__(self, row, col, color, image):
        super().__init__(row, col, color, image)

    def find_legal_moves(self, board):
        legal_moves = {}
        # ROOK MOVEMENT:
        legal_moves.update(self.find_top_moves(board))
        legal_moves.update(self.find_bottom_moves(board))
        legal_moves.update(self.find_right_moves(board))
        legal_moves.update(self.find_left_moves(board))
        # BISHOP MOVEMENT:
        legal_moves.update(self.find_top_left_diagonal_moves(board))
        legal_moves.update(self.find_top_right_diagonal_moves(board))
        legal_moves.update(self.find_bottom_left_diagonal_moves(board))
        legal_moves.update(self.find_bottom_right_diagonal_moves(board))
        return legal_moves

