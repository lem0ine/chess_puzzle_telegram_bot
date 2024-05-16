import chess
import chess.svg
import cairosvg

class ChessPuzzle:
    def __init__(self, fen, moves):
        self.board = chess.Board(fen)
        self.solution_moves = moves
        print(f"Initial FEN: {self.board.fen()}")
        if self.solution_moves:
            self.board.push_uci(self.solution_moves.pop(0))
        print(f"FEN after opponent's move: {self.board.fen()}")

    def generate_puzzle(self):
        svg_image = chess.svg.board(self.board, size=350)
        png_image = cairosvg.svg2png(bytestring=svg_image)
        return png_image

    def check_move(self, move):
        try:
            print(f"Current FEN: {self.board.fen()}")
            print(f"User move: {move}")

            try:
                chess_move = self.board.parse_san(move)
            except ValueError as e:
                print(f"Error parsing move: {e}")
                return False, "Некорректная нотация хода"

            uci_move = chess_move.uci()
            print(f"Parsed UCI move: {uci_move}")

            if not self.solution_moves:
                print("No more moves expected")
                return False, "Нет ожидаемых ходов."

            correct_move = self.solution_moves[0]
            print(f"Expected UCI move: {correct_move}")

            if uci_move == correct_move:
                self.board.push(chess_move)
                self.solution_moves.pop(0)
                print(f"Move executed. New FEN: {self.board.fen()}")
                if not self.solution_moves:
                    return True, "Поздравляем! Вы решили задачу."
                return True, "Ход корректен, продолжайте."
            else:
                print(f"Некорректный ход: {uci_move}, ожидалось: {correct_move}")
                return False, f"Некорректный ход: {uci_move}, ожидалось: {correct_move}"
        except chess.IllegalMoveError as e:
            print(f"Illegal move: {e}")
            return False, "Нелегальный ход"

    def make_opponent_move(self):
        if self.solution_moves:
            opponent_move = self.solution_moves.pop(0)
            print(f"Making opponent move: {opponent_move}")
            print(f"Current FEN before opponent move: {self.board.fen()}")
            self.board.push_uci(opponent_move)
            print(f"Current FEN after opponent move: {self.board.fen()}")

    def update_board(self):
        return chess.svg.board(self.board, size=350)

    def get_current_player(self):
        return "белых" if self.board.turn == chess.WHITE else "черных"
