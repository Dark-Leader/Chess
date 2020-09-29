from .constants import (ROWS, COLS, BLACK, WHITE, SQUARE_SIZE, BLACK_KING, BLACK_ROOK, BLACK_PAWN, BLACK_BISHOP,
                        BLACK_QUEEN, BLACK_KNIGHT, WHITE_BISHOP, WHITE_PAWN, WHITE_QUEEN, WHITE_ROOK, WHITE_KING,
                        WHITE_KNIGHT, DARK_SQUARE)
from .pieces.rook import Rook
from .pieces.bishop import Bishop
from .pieces.knight import Knight
from .pieces.king import King
from .pieces.queen import Queen
from .pieces.pawn import Pawn
import pygame


class Board:

    def __init__(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self._initialize_board()
        self.valid_moves = {}

    def _initialize_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (col == 0 and row == 0) or (col == 7 and row == 0):
                    self.board[row][col] = Rook(row, col, BLACK, BLACK_ROOK)
                elif (col == 0 and row == 7) or (col == 7 and row == 7):
                    self.board[row][col] = Rook(row, col, WHITE, WHITE_ROOK)
                elif row == 0 and (col == 1 or col == 6):
                    self.board[row][col] = Knight(row, col, BLACK, BLACK_KNIGHT)
                elif row == 7 and (col == 1 or col == 6):
                    self.board[row][col] = Knight(row, col, WHITE, WHITE_KNIGHT)
                elif row == 0 and (col == 2 or col == 5):
                    self.board[row][col] = Bishop(row, col, BLACK, BLACK_BISHOP)
                elif row == 7 and (col == 2 or col == 5):
                    self.board[row][col] = Bishop(row, col, WHITE, WHITE_BISHOP)
                elif row == 0 and col == 3:
                    self.board[row][col] = Queen(row, col, BLACK, BLACK_QUEEN)
                elif row == 7 and col == 3:
                    self.board[row][col] = Queen(row, col, WHITE, WHITE_QUEEN)
                elif row == 0 and col == 4:
                    self.board[row][col] = King(row, col, BLACK, BLACK_KING)
                elif row == 7 and col == 4:
                    self.board[row][col] = King(row, col, WHITE, WHITE_KING)
                elif row == 1:
                    self.board[row][col] = Pawn(row, col, BLACK, BLACK_PAWN)
                elif row == 6:
                    self.board[row][col] = Pawn(row, col, WHITE, WHITE_PAWN)
                else:
                    self.board[row][col] = None

    def draw(self, win):
        win.fill(DARK_SQUARE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (SQUARE_SIZE * col, SQUARE_SIZE * row, SQUARE_SIZE, SQUARE_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    piece.draw(win)

    def get_piece(self, row, col):
        return self.board[row][col]

    @staticmethod
    def move(piece, row, col, array):
        start_row = piece.get_row()
        start_col = piece.get_col()
        array[start_row][start_col], array[row][col] = None, array[start_row][start_col]
        piece.move(row, col)

    def find_legal_moves(self, piece):
        self.valid_moves = piece.find_legal_moves(self.board)
        row, col = piece.get_row(), piece.get_col()
        self.remove_illegal_moves(row, col)
        return self.valid_moves

    @staticmethod
    def find_king(color, board):
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if isinstance(piece, King) and piece.get_color() == color and piece is not None:
                    return piece

    @staticmethod
    def check(king, board):
        king_row, king_col = king.get_row(), king.get_col()
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece is not None and piece.get_color() != king.get_color() and \
                        (king_row, king_col) in piece.find_legal_moves(board):
                    return True
        return False

    def remove_illegal_moves(self, row, col):
        bad_moves = []
        color = self.get_piece(row, col).get_color()
        for move, captured in self.valid_moves.items():
            copy_board = self.copy_board()
            piece = copy_board[row][col]
            end_row, end_col = move
            if captured:
                self._remove(copy_board, captured)
            self.move(piece, end_row, end_col, copy_board)
            king = self.find_king(color, copy_board)
            if self.check(king, copy_board):
                bad_moves.append(move)
        for move in bad_moves:
            self.valid_moves.pop(move)

    def copy_board(self):
        temp_board = [[None] * COLS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if isinstance(piece, Pawn):
                    temp_board[row][col] = Pawn(row, col, piece.get_color(), piece.image)
                elif isinstance(piece, Bishop):
                    temp_board[row][col] = Bishop(row, col, piece.get_color(), piece.image)
                elif isinstance(piece, Knight):
                    temp_board[row][col] = Knight(row, col, piece.get_color(), piece.image)
                elif isinstance(piece, Rook):
                    temp_board[row][col] = Rook(row, col, piece.get_color(), piece.image)
                elif isinstance(piece, Queen):
                    temp_board[row][col] = Queen(row, col, piece.get_color(), piece.image)
                elif isinstance(piece, King):
                    temp_board[row][col] = King(row, col, piece.get_color(), piece.image)
                else:
                    temp_board[row][col] = None
        return temp_board

    @staticmethod
    def _remove(board, position):
        row, col = position
        board[row][col] = None
