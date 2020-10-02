from .piece import Piece
from chess.constants import ROWS, COLS, WHITE


class Knight(Piece):

    def __init__(self, row, col, color, image):
        super().__init__(row, col, color, image)

    def find_legal_moves(self, board):
        legal_moves = {}
        row = self.row
        col = self.col

        # top - left:
        if row >= 2 and col >= 1:
            legal_moves.update(self.check_valid_square(row - 2, col - 1, board))

        # top - right:
        if row >= 2 and col <= COLS - 2:
            legal_moves.update(self.check_valid_square(row - 2, col + 1, board))

        # left - top:
        if row >= 1 and col >= 2:
            legal_moves.update(self.check_valid_square(row - 1, col - 2, board))

        # left - bottom:
        if row <= ROWS - 2 and col >= 2:
            legal_moves.update(self.check_valid_square(row + 1, col - 2, board))

        # bottom - left:
        if row <= ROWS - 3 and col >= 1:
            legal_moves.update(self.check_valid_square(row + 2, col - 1, board))

        # bottom - right:
        if row <= ROWS - 3 and col <= COLS - 2:
            legal_moves.update(self.check_valid_square(row + 2, col + 1, board))

        # right - top:
        if row >= 1 and col <= COLS - 3:
            legal_moves.update(self.check_valid_square(row - 1, col + 2, board))

        # right - bottom:
        if row <= ROWS - 2 and col <= COLS - 3:
            legal_moves.update(self.check_valid_square(row + 1, col + 2, board))

        return legal_moves

    def check_valid_square(self, row, col, board):
        legal_moves = {}
        possible_square = board[row][col]
        if possible_square is None:
            legal_moves[(row, col)] = []
        elif possible_square is not None and possible_square.get_color() != self.color:
            legal_moves[(row, col)] = (row, col)
        return legal_moves

    def to_fen(self):
        if self.color == WHITE:
            return "N"
        else:
            return "n"
