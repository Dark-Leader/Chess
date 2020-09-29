from chess.pieces.piece import Piece
from chess.constants import WHITE, ROWS, COLS


class Pawn(Piece):

    def __init__(self, row, col, color, image):
        super().__init__(row, col, color, image)
        self.can_be_captured_en_passant = False

    def find_legal_moves(self, board):
        if self.color == WHITE:
            return self.find_white_legal_moves(board)
        return self.find_black_legal_moves(board)

    def move(self, new_row, new_col):
        if abs(new_row - self.row) == 2:
            self.can_be_captured_en_passant = True
        return super().move(new_row, new_col)

    def find_white_legal_moves(self, board):
        legal_moves = {}
        row = self.row
        top = self.row - 1
        col = self.col
        left = col - 1
        right = col + 1

        if top >= 0:
            top_piece = board[top][col]
            if top_piece is None:
                legal_moves[(top, col)] = []
            if left >= 0:
                top_left = board[top][left]
                if top_left is not None and top_left.get_color() != self.color:
                    legal_moves[(top, left)] = (top, left)
            if right <= COLS - 1:
                top_right = board[top][right]
                if top_right is not None and top_right.get_color() != self.color:
                    legal_moves[(top, right)] = (top, right)
            if row == 6:
                if top_piece is None and board[top - 1][col] is None:
                    legal_moves[(top - 1, col)] = []
        # en passant
        if row == 3:
            if left >= 0:
                piece_left = board[row][left]
                if isinstance(piece_left, Pawn) and piece_left.get_color() != self.color and \
                        piece_left.can_be_captured_en_passant:
                    legal_moves[(top, left)] = (row, left)
            if right <= COLS - 1:
                piece_right = board[row][right]
                if isinstance(piece_right, Pawn) and piece_right.get_color() != self.color and \
                        piece_right.can_be_captured_en_passant:
                    legal_moves[(top, right)] = (row, right)
        return legal_moves

    def find_black_legal_moves(self, board):
        legal_moves = {}
        row = self.row
        bottom = self.row + 1
        col = self.col
        left = col - 1
        right = col + 1
        if bottom <= ROWS - 1:
            bottom_piece = board[bottom][col]
            if bottom_piece is None:
                legal_moves[(bottom, col)] = []
            if left >= 0:
                bottom_left = board[bottom][left]
                if bottom_left is not None and bottom_left.get_color() != self.color:
                    legal_moves[(bottom, left)] = (bottom, left)
            if right <= COLS - 1:
                bottom_right = board[bottom][right]
                if bottom_right is not None and bottom_right.get_color() != self.color:
                    legal_moves[(bottom, right)] = (bottom, right)
            if row == 1 and bottom_piece is None:
                piece_below = board[bottom + 1][col]
                if piece_below is None:
                    legal_moves[(bottom + 1, col)] = []
        # en passant
        if row == 4:
            if left >= 0:
                piece_left = board[row][left]
                if isinstance(piece_left, Pawn) and piece_left.get_color() != self.color and \
                        piece_left.can_be_captured_en_passant:
                    legal_moves[(bottom, left)] = (row, left)
            if right <= COLS - 1:
                piece_right = board[row][right]
                if isinstance(piece_right, Pawn) and piece_right.get_color() != self.color and \
                        piece_right.can_be_captured_en_passant:
                    legal_moves[(bottom, right)] = (row, right)
        return legal_moves
