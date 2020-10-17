from .constants import (ROWS, COLS, BLACK, WHITE, SQUARE_SIZE, BLACK_KING, BLACK_ROOK, BLACK_PAWN, BLACK_BISHOP,
                        BLACK_QUEEN, BLACK_KNIGHT, WHITE_BISHOP, WHITE_PAWN, WHITE_QUEEN, WHITE_ROOK, WHITE_KING,
                        WHITE_KNIGHT, DARK_SQUARE, BOARD_EDGE, LIGHT_BLUE, HEIGHT, TEXT_OFFSET)
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
        self.promotion_move = False

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
        win.fill(LIGHT_BLUE)
        for row in range(ROWS):
            for col in range(COLS):
                if row % 2 == 0 and col % 2 == 0:
                    pygame.draw.rect(win, WHITE, (SQUARE_SIZE * col + BOARD_EDGE, SQUARE_SIZE * row + BOARD_EDGE,
                                                  SQUARE_SIZE, SQUARE_SIZE))
                elif row % 2 == 0 and col % 2 == 1:
                    pygame.draw.rect(win, DARK_SQUARE, (SQUARE_SIZE * col + BOARD_EDGE, SQUARE_SIZE * row + BOARD_EDGE,
                                                        SQUARE_SIZE, SQUARE_SIZE))
                elif row % 2 == 1 and col % 2 == 0:
                    pygame.draw.rect(win, DARK_SQUARE, (SQUARE_SIZE * col + BOARD_EDGE, SQUARE_SIZE * row + BOARD_EDGE,
                                                        SQUARE_SIZE, SQUARE_SIZE))
                else:
                    pygame.draw.rect(win, WHITE, (SQUARE_SIZE * col + BOARD_EDGE, SQUARE_SIZE * row + BOARD_EDGE,
                                                  SQUARE_SIZE, SQUARE_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    piece.draw(win)

        col_letters = {0: "A",
                       1: "B",
                       2: "C",
                       3: "D",
                       4: "E",
                       5: "F",
                       6: "G",
                       7: "H"}
        row_numbers = [i for i in range(1, 9)]
        for index, col in col_letters.items():
            font = pygame.font.Font(None, 24)
            text = font.render(col, 1, BLACK)
            win.blit(text, (SQUARE_SIZE * index + BOARD_EDGE + SQUARE_SIZE * 0.5 - TEXT_OFFSET // 2, TEXT_OFFSET // 2))
            win.blit(text, (SQUARE_SIZE * index + BOARD_EDGE + SQUARE_SIZE * 0.5 - TEXT_OFFSET // 2,
                            HEIGHT + BOARD_EDGE + TEXT_OFFSET // 2))
        for row in row_numbers:
            font = pygame.font.Font(None, 24)
            text = font.render(str(row), 1, BLACK)
            win.blit(text, (TEXT_OFFSET, HEIGHT - (BOARD_EDGE + (row - 1) * SQUARE_SIZE + TEXT_OFFSET // 2)))
            win.blit(text, (SQUARE_SIZE * 8 + BOARD_EDGE + TEXT_OFFSET,
                            HEIGHT - (BOARD_EDGE + (row - 1) * SQUARE_SIZE + TEXT_OFFSET // 2)))

    def get_piece(self, row, col):
        return self.board[row][col]

    def move(self, piece, row, col, array):
        start_row = piece.get_row()
        start_col = piece.get_col()
        array[start_row][start_col], array[row][col] = None, array[start_row][start_col]
        piece.move(row, col)
        if isinstance(piece, King) and col == start_col + 2 and not \
                self.check(start_row, start_col, piece.get_color(), array):  # short_castle
            self.short_castle(start_row, array)
        elif isinstance(piece, King) and col == start_col - 2 and not \
                self.check(start_row, start_col, piece.get_color(), array):  # long_castle
            self.long_castle(start_row, array)
        elif isinstance(piece, Pawn) and (row == 0) and array == self.board:  # pawn promotion move
            self.promotion_move = (row, col)

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
                if isinstance(piece, King) and piece.get_color() == color:
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
            king = self.find_king(color, copy_board)
            if captured:
                self.remove(copy_board, captured)
            self.move(new_piece, end_row, end_col, copy_board)
            king_row, king_col, king_color = king.get_row(), king.get_col(), king.get_color()
            if self.check(king_row, king_col, king_color, copy_board):
                bad_moves.append(move)
            if isinstance(piece, King) and end_col == piece.get_col() + 2:  # short castle
                if self.check(piece.get_row(), piece.get_col() + 1, color, copy_board):
                    bad_moves.append(move)
                elif self.check(piece.get_row(), piece.get_col(), piece.get_color(), copy_board):
                    bad_moves.append(move)
            if isinstance(piece, King) and end_col == piece.get_col() - 2:  # long castle
                if self.check(piece.get_row(), piece.get_col() - 1, color, copy_board):
                    bad_moves.append(move)
                elif self.check(piece.get_row(), piece.get_col(), piece.get_color(), copy_board):
                    bad_moves.append(move)
        for move in bad_moves:
            if move in moves:
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
                if isinstance(piece, Pawn) and piece.get_color() != color and piece.can_be_captured_en_passant:
                    piece.can_be_captured_en_passant = False

    def short_castle(self, row, board):
        rook = board[row][COLS - 1]
        if rook:
            self.move(rook, row, COLS - 3, board)

    def long_castle(self, row, board):
        rook = board[row][0]
        if rook:
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
                    current = piece.find_legal_moves(self.board)
                    self.remove_illegal_moves(row, col, current)
                    moves.update(current)
        # might be overridden mid traversal above so we check again the king legal moves
        king = self.find_king(color, self.board)
        row, col = king.get_row(), king.get_col()
        king_moves = king.find_legal_moves(self.board)
        self.remove_illegal_moves(row, col, king_moves)
        moves.update(king_moves)
        self.all_possible_moves = moves

    def get_fen(self, turn, half_moves, full_moves):
        cols = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        fen = ""
        en_passant = False
        white_king_side_castle = True
        white_queen_side_castle = True
        black_king_side_castle = True
        black_queen_side_castle = True
        for row in range(ROWS):
            count = 0
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    if count:
                        fen += str(count)
                        count = 0
                    if isinstance(piece, Pawn) and piece.can_be_captured_en_passant:
                        if piece.get_color() == WHITE:
                            en_passant = (row - 1, col)
                        else:
                            en_passant = (row + 3, col)
                    fen += piece.to_fen()
                else:
                    count += 1
            if count > 0:
                fen += str(count)
            if row != ROWS - 1:
                fen += "/"
        if turn == WHITE:
            fen += " w "
        else:
            fen += " b "
        # check castling rights
        white_king = self.find_king(WHITE, self.board)
        black_king = self.find_king(BLACK, self.board)
        if white_king.moved_before:
            white_king_side_castle = False
            white_queen_side_castle = False
        if black_king.moved_before:
            black_king_side_castle = False
            black_queen_side_castle = False
        white_short_castle_rook = self.board[ROWS - 1][COLS - 1]
        if white_short_castle_rook is None or not isinstance(white_short_castle_rook, Rook):
            white_king_side_castle = False
        elif isinstance(white_short_castle_rook, Rook) and white_short_castle_rook.moved_before or \
            white_short_castle_rook.get_color() != WHITE:
            white_king_side_castle = False

        white_long_castle_rook = self.board[ROWS - 1][0]
        if white_long_castle_rook is None or not isinstance(white_long_castle_rook, Rook):
            white_queen_side_castle = False
        elif isinstance(white_long_castle_rook, Rook) and white_long_castle_rook.moved_before or \
            white_long_castle_rook.get_color() != WHITE:
            white_queen_side_castle = False

        black_short_castle_rook = self.board[0][COLS - 1]
        if black_short_castle_rook is None or not isinstance(black_short_castle_rook, Rook):
            black_king_side_castle = False
        elif isinstance(black_short_castle_rook, Rook) and black_short_castle_rook.moved_before or \
            black_short_castle_rook.get_color() != BLACK:
            black_king_side_castle = False

        black_long_castle_rook = self.board[0][0]
        if black_long_castle_rook is None or not isinstance(black_long_castle_rook, Rook):
            black_queen_side_castle = False
        elif isinstance(black_long_castle_rook, Rook) and black_long_castle_rook.moved_before or \
            black_long_castle_rook.get_color() != BLACK:
            black_queen_side_castle = False

        if white_king_side_castle:
            fen += "K"
        if white_queen_side_castle:
            fen += "Q"
        if black_king_side_castle:
            fen += "k"
        if black_queen_side_castle:
            fen += "q"
        if not (white_king_side_castle or white_queen_side_castle) and not \
                (black_king_side_castle or black_queen_side_castle):
            fen += "-"
        fen += " "

        if en_passant:
            row, col = en_passant
            col = cols[col]
            fen += f"{col}{row} "
        else:
            fen += "- "
        fen += f"{half_moves} {full_moves}"
        return fen

    def get_position(self):
        fen = ""
        for row in range(ROWS):
            count = 0
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    if count:
                        fen += str(count)
                        count = 0
                    fen += piece.to_fen()
                else:
                    count += 1
            if count > 0:
                fen += str(count)
            if row != ROWS - 1:
                fen += "/"
        return fen

    def reset(self):
        self._initialize_board()
        self.valid_moves = {}
        self.all_possible_moves = {}
        self.winner = None
        self.promotion_move = False

    def print_board_to_console(self):
        board_width = 21
        rows = [i for i in range(8, 0, - 1)]
        cols = " ".join([chr(i) for i in range(65, 73)])
        print("-" * board_width)
        print(f"   {cols}")
        for row in range(ROWS):
            print(f"{rows[row]} |", end="")
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    print(f"{piece.to_fen()}|", end="")
                else:
                    print(" |", end="")
            print(f" {rows[row]}")
        print(f"   {cols}")
        print("-" * board_width)

