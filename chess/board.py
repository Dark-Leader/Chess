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
        self.all_possible_moves = {}
        self.winner = None

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

    def move(self, piece, row, col, array):
        start_row = piece.get_row()
        start_col = piece.get_col()
        array[start_row][start_col], array[row][col] = None, array[start_row][start_col]
        piece.move(row, col)
        if isinstance(piece, King) and col == start_col + 2:  # short_castle
            self.short_castle(start_row, array)
        elif isinstance(piece, King) and col == start_col - 2:  # long_castle
            self.long_castle(start_row, array)

    def find_legal_moves(self, piece):
        self.valid_moves = piece.find_legal_moves(self.board)
        row, col = piece.get_row(), piece.get_col()
        self.remove_illegal_moves(row, col, self.valid_moves)
        return self.valid_moves

    @staticmethod
    def find_king(color, board):
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if isinstance(piece, King) and piece.get_color() == color and piece is not None:
                    return piece

    @staticmethod
    def check(king_row, king_col, king_color, board):
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece is not None and piece.get_color() != king_color and \
                        (king_row, king_col) in piece.find_legal_moves(board):
                    return True
        return False

    def remove_illegal_moves(self, row, col, moves):
        bad_moves = []
        piece = self.get_piece(row, col)
        color = piece.get_color()
        for move, captured in moves.items():
            copy_board = self.copy_board()
            new_piece = copy_board[row][col]
            end_row, end_col = move
            if captured:
                self.remove(copy_board, captured)
            self.move(new_piece, end_row, end_col, copy_board)
            king = self.find_king(color, copy_board)
            king_row, king_col, king_color = king.get_row(), king.get_col(), king.get_color()
            if self.check(king_row, king_col, king_color, copy_board):
                bad_moves.append(move)
            if isinstance(piece, King) and end_col == piece.get_col() + 2:  # short castle
                if self.check(piece.get_row(), piece.get_col() + 1, color, copy_board):
                    bad_moves.append(move)
            if isinstance(piece, King) and end_col == piece.get_col() - 2:  # long castle
                if self.check(piece.get_row(), piece.get_col() - 1, color, copy_board):
                    bad_moves.append(move)
        for move in bad_moves:
            moves.pop(move)

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
    def remove(board, position):
        row, col = position
        board[row][col] = None

    def stop_en_passant(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if isinstance(piece, Pawn) and piece.get_color() != color:
                    piece.change_en_passant_status()
                    
    def short_castle(self, row, board):
        rook = board[row][COLS - 1]
        self.move(rook, row, COLS - 3, board)

    def long_castle(self, row, board):
        rook = board[row][0]
        self.move(rook, row, 3, board)

    def checkmate_or_stalemate(self, color):
        king = self.find_king(color, self.board)
        row, col, color = king.get_row(), king.get_col(), king.get_color()
        if not bool(self.all_possible_moves):
            if self.check(row, col, color, self.board):
                if color == WHITE:
                    return "Black Won"
                elif color == BLACK:
                    return "White Won"
            else:
                return "Stalemate"
        return None

    def find_all_possible_moves(self, color):
        moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece is not None and piece.get_color() == color:
                    moves.update(piece.find_legal_moves(self.board))
                    self.remove_illegal_moves(row, col, moves)
        self.all_possible_moves = moves
