from stockfish import Stockfish
from chess.constants import ENGINE_DEPTH, ENGINE_STRENGTH


class Engine:

    def __init__(self, skill_level):
        parameters = {
            "Write Debug Log": "false",
            "Contempt": 0,
            "Min Split Depth": 0,
            "Threads": 1,
            "Ponder": "false",
            "Hash": 16,
            "MultiPV": 1,
            "Skill Level": skill_level,
            "Move Overhead": 30,
            "Minimum Thinking Time": 20,
            "Slow Mover": 80,
            "UCI_Chess960": "false",
        }
        self.engine = Stockfish("resources/stockfish.exe", parameters=parameters)
        self.engine.set_depth(ENGINE_DEPTH)

    def set_position(self, fen):
        self.engine.set_fen_position(fen)

    def get_move(self, time):
        return self.engine.get_best_move_time(time)
