from chess.board import Board
from chess.constants import (WHITE, BLACK, LIGHT_BLUE, SQUARE_SIZE, POSSIBLE_MOVE_RADIUS, BOARD_EDGE, HEIGHT, WIDTH,
                             RED, BLUE, GREEN, ORANGE)
from chess.shapes.button import Button
from chess.pieces.pawn import Pawn
import pygame


class Game:

    def __init__(self, win):
        self.win = win
        self._initialize()

    def _initialize(self):
        self.board = Board()
        self.selected = None
        self.turn = WHITE
        self.valid_moves = {}
        self.winner = None
        self.moves_since_pawn_move_or_capture = 0
        self.past_positions = {self.board.get_position(): 1}
        self.move_count = 0
        self.promotion_move = False
        self.buttons = [Button(SQUARE_SIZE * 9, SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE // 2, RED, "queen"),
                        Button(SQUARE_SIZE * 9, SQUARE_SIZE * 2, SQUARE_SIZE, SQUARE_SIZE // 2, BLUE, "bishop"),
                        Button(SQUARE_SIZE * 9, SQUARE_SIZE * 3, SQUARE_SIZE, SQUARE_SIZE // 2, GREEN, "knight"),
                        Button(SQUARE_SIZE * 9, SQUARE_SIZE * 4, SQUARE_SIZE, SQUARE_SIZE // 2, ORANGE, "rook")]

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves()
        if self.promotion_move:
            for button in self.buttons:
                button.draw(self.win)

    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.win, LIGHT_BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2 + BOARD_EDGE,
                               row * SQUARE_SIZE + SQUARE_SIZE // 2 + BOARD_EDGE), POSSIBLE_MOVE_RADIUS)

    def select(self, position):
        pos = self.get_position(position)
        if pos and not self.promotion_move:
            row, col = pos
            if self.selected:
                result = self._move(row, col)
                if not result:
                    self.selected = None
                    self.select(position)
                    self.valid_moves = {}
            piece = self.board.get_piece(row, col)
            if piece is not None and piece.get_color() == self.turn:
                self.selected = piece
                self.valid_moves = self.board.find_legal_moves(piece)
                return True
        elif self.promotion_move:
            row, col = self.promotion_move
            for button in self.buttons:
                if button.clicked(position):
                    piece_type = button.get_name()
                    piece = self.board.get_piece(row, col)
                    if piece_type == "queen":
                        self.board.board[row][col] = piece.promote_to_queen()
                    elif piece_type == "bishop":
                        self.board.board[row][col] = piece.promote_to_bishop()
                    elif piece_type == "knight":
                        self.board.board[row][col] = piece.promote_to_knight()
                    elif piece_type == "rook":
                        self.board.board[row][col] = piece.promote_to_rook()
            self.promotion_move = False
            self.board.promotion_move = False
            self.update_past_positions()
            board_pos = self.board.get_position()
            self.change_turn(board_pos)
            self.moves_since_pawn_move_or_capture = 0
        return False

    @staticmethod
    def get_position(position):
        x, y = position
        if BOARD_EDGE <= x <= WIDTH + BOARD_EDGE and BOARD_EDGE <= y <= HEIGHT + BOARD_EDGE:
            row = (y - BOARD_EDGE) // SQUARE_SIZE
            col = (x - BOARD_EDGE) // SQUARE_SIZE
            return row, col
        else:
            return None

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col, self.board.board)
            capture = self.valid_moves[(row, col)]
            if capture:
                self.moves_since_pawn_move_or_capture = 0
                capture_row, capture_col = capture
                if capture_row != row:  # en passant
                    self.board.remove(self.board.board, capture)
            elif isinstance(self.selected, Pawn):
                self.moves_since_pawn_move_or_capture = 0
            else:
                self.moves_since_pawn_move_or_capture += 1
            position = self.board.get_position()
            self.promotion_move = self.board.promotion_move
            if not self.promotion_move:
                self.update_past_positions()
                self.change_turn(position)
            # print(f"move: {self.move_count}")
            print(self.board.get_fen(self.turn))
            # print(self.board.get_position())
        else:
            return False
        return True

    def change_turn(self, position):
        self.valid_moves = {}
        self.board.stop_en_passant(self.turn)
        if self.turn == WHITE:
            self.turn = BLACK
            self.move_count += 1
        else:
            self.turn = WHITE
        self.board.find_all_possible_moves(self.turn)
        if self.moves_since_pawn_move_or_capture == 100:
            self.winner = "Draw - 50 move rule"
        elif self.past_positions[position] == 3:
            self.winner = "Draw - 3 fold repetition"
        else:
            self.winner = self.board.checkmate_or_stalemate(self.turn)

    def reset(self):
        self._initialize()

    def get_winner(self):
        return self.winner

    def check_promotion(self):
        piece = self.board.promotion_move
        if piece:
            self.board.promotion_move = False
            return piece
        return False

    def update_past_positions(self):
        position = self.board.get_position()
        if position in self.past_positions:
            self.past_positions[position] += 1
        else:
            self.past_positions[position] = 1
