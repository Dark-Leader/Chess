from chess.constants import SQUARE_SIZE, ROWS, COLS


class Piece:

    def __init__(self, row, col, color, image):
        self.row = row
        self.col = col
        self.color = color
        self.image = image
        self.pinned = False

    def move(self, new_row, new_col):
        self.set_row(new_row)
        self.set_col(new_col)

    def draw(self, win):
        win.blit(self.image, (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE))
        
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def get_color(self):
        return self.color
    
    def set_row(self, row):
        self.row = row
        
    def set_col(self, col):
        self.col = col

    def find_top_left_diagonal_moves(self, board):
        legal_moves = {}
        top = self.row - 1
        left = self.col - 1
        while top >= 0 and left >= 0:
            piece = board[top][left]
            if piece is not None and piece.get_color() == self.color:
                break
            elif piece is not None and piece.get_color() != self.color:
                legal_moves[top, left] = (top, left)
                break
            elif piece is None:
                legal_moves[(top, left)] = []
            top -= 1
            left -= 1
        return legal_moves

    def find_top_right_diagonal_moves(self, board):
        legal_moves = {}
        top = self.row - 1
        right = self.col + 1
        while top >= 0 and right <= COLS - 1:
            piece = board[top][right]
            if piece is not None and piece.get_color() == self.color:
                break
            elif piece is not None and piece.get_color() != self.color:
                legal_moves[(top, right)] = (top, right)
                break
            elif piece is None:
                legal_moves[(top, right)] = []
            top -= 1
            right += 1
        return legal_moves

    def find_bottom_left_diagonal_moves(self, board):
        legal_moves = {}
        bottom = self.row + 1
        left = self.col - 1
        while bottom <= ROWS - 1 and left >= 0:
            piece = board[bottom][left]
            if piece is not None and piece.get_color() == self.color:
                break
            elif piece is not None and piece.get_color() != self.color:
                legal_moves[(bottom, left)] = (bottom, left)
                break
            elif piece is None:
                legal_moves[(bottom, left)] = []
            bottom += 1
            left -= 1
        return legal_moves

    def find_bottom_right_diagonal_moves(self, board):
        legal_moves = {}
        bottom = self.row + 1
        right = self.col + 1
        while bottom <= ROWS - 1 and right <= COLS - 1:
            piece = board[bottom][right]
            if piece is not None and piece.get_color() == self.color:
                break
            elif piece is not None and piece.get_color() != self.color:
                legal_moves[(bottom, right)] = (bottom, right)
                break
            elif piece is None:
                legal_moves[(bottom, right)] = []
            bottom += 1
            right += 1
        return legal_moves

    def find_top_moves(self, board):
        legal_moves = {}
        top = self.row - 1
        while top >= 0:
            top_piece = board[top][self.col]
            if top_piece is not None and top_piece.get_color() == self.color:
                break
            elif top_piece is not None and top_piece.get_color() != self.color:
                legal_moves[(top, self.col)] = (top, self.col)
                break
            elif top_piece is None:
                legal_moves[(top, self.col)] = []
            top -= 1
        return legal_moves

    def find_bottom_moves(self, board):
        legal_moves = {}
        bottom = self.row + 1
        while bottom <= ROWS - 1:
            bottom_piece = board[bottom][self.col]
            if bottom_piece is not None and bottom_piece.get_color() == self.color:
                break
            elif bottom_piece is not None and bottom_piece.get_color() != self.color:
                legal_moves[(bottom, self.col)] = (bottom, self.col)
                break
            elif bottom_piece is None:
                legal_moves[(bottom, self.col)] = []
            bottom += 1
        return legal_moves

    def find_right_moves(self, board):
        legal_moves = {}
        right = self.col + 1
        while right <= COLS - 1:
            right_piece = board[self.row][right]
            if right_piece is not None and right_piece.get_color() == self.color:
                break
            elif right_piece is not None and right_piece.get_color() != self.color:
                legal_moves[(self.row, right)] = (self.row, right)
                break
            elif right_piece is None:
                legal_moves[(self.row, right)] = []
            right += 1
        return legal_moves

    def find_left_moves(self, board):
        legal_moves = {}
        left = self.col - 1
        while left >= 0:
            left_piece = board[self.row][left]
            if left_piece is not None and left_piece.get_color() == self.color:
                break
            elif left_piece is not None and left_piece.get_color() != self.color:
                legal_moves[(self.row, left)] = (self.row, left)
                break
            elif left_piece is None:
                legal_moves[(self.row, left)] = []
            left -= 1
        return legal_moves

    def __str__(self):
        return f"row = {self.row}, col = {self.col}, color = {self.color}, {type(self)}"