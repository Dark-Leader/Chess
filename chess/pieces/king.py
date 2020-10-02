from .piece import Piece
from chess.constants import ROWS, COLS, WHITE
from .rook import Rook


class King(Piece):

    def __init__(self, row, col, color, image):
        super().__init__(row, col, color, image)
        self.moved_before = False

    def find_legal_moves(self, board):
        legal_moves = {}
        row = self.row
        col = self.col
        top = row - 1
        bottom = row + 1
        left = col - 1
        right = col + 1
        if top >= 0:
            if left >= 0:  # top left
                top_left = board[top][left]
                if top_left is None:
                    legal_moves[(top, left)] = []
                elif top_left is not None and top_left.get_color() != self.color:
                    legal_moves[(top, left)] = (top, left)
            # top
            top_piece = board[top][col]
            if top_piece is None:
                legal_moves[(top, col)] = []
            elif top_piece is not None and top_piece.get_color() != self.color:
                legal_moves[(top, col)] = (top, col)
            # top right
            if right <= COLS - 1:
                top_right = board[top][right]
                if top_right is None:
                    legal_moves[(top, right)] = []
                elif top_right is not None and top_right.get_color() != self.color:
                    legal_moves[(top, right)] = (top, right)

        if bottom <= ROWS - 1:
            if left >= 0:  # bottom left
                bottom_left = board[bottom][left]
                if bottom_left is None:
                    legal_moves[(bottom, left)] = []
                elif bottom_left is not None and bottom_left.get_color() != self.color:
                    legal_moves[(bottom, left)] = (bottom, left)
            # bottom
            bottom_piece = board[bottom][col]
            if bottom_piece is None:
                legal_moves[(bottom, col)] = []
            elif bottom_piece is not None and bottom_piece.get_color() != self.color:
                legal_moves[(bottom, col)] = (bottom, col)
            # bottom right
            if right <= COLS - 1:
                bottom_right = board[bottom][right]
                if bottom_right is None:
                    legal_moves[(bottom, right)] = []
                elif bottom_right is not None and bottom_right.get_color() != self.color:
                    legal_moves[(bottom, right)] = (bottom, right)
        # right
        if right <= COLS - 1:
            right_piece = board[row][right]
            if right_piece is None:
                legal_moves[(row, right)] = []
            elif right_piece is not None and right_piece.get_color() != self.color:
                legal_moves[(row, right)] = (row, right)
        # left
        if left >= 0:
            left_piece = board[row][left]
            if left_piece is None:
                legal_moves[(row, left)] = []
            elif left_piece is not None and left_piece.get_color() != self.color:
                legal_moves[(row, left)] = (row, left)
                
        legal_moves.update(self.check_short_castle_rights(board))
        legal_moves.update(self.check_long_castle_rights(board))
        return legal_moves

    def check_short_castle_rights(self, board):
        moves = {}
        if self.moved_before:
            return moves
        king_col = self.col
        for col in range(king_col + 1, COLS - 1):
            if board[self.row][col] is not None:
                return moves
        rook = board[self.row][COLS - 1]
        if isinstance(rook, Rook) and rook.get_color() == self.color and not rook.moved_before:
            moves[(self.row, self.col + 2)] = []
        return moves

    def check_long_castle_rights(self, board):
        moves = {}
        if self.moved_before:
            return moves
        king_col = self.col
        for col in range(king_col - 1, 0, -1):
            if board[self.row][col] is not None:
                return moves
        rook = board[self.row][0]
        if isinstance(rook, Rook) and rook.get_color() == self.color and not rook.moved_before:
            moves[(self.row, self.col - 2)] = []
        return moves

    def move(self, row, col):
        super().move(row, col)
        self.moved_before = True

    def to_fen(self):
        if self.color == WHITE:
            return "K"
        else:
            return "k"
