import pandas as pd
import zstandard as zstd
import io
import random

def read_zst_csv(file_path):
    dctx = zstd.ZstdDecompressor()
    with open(file_path, 'rb') as f:
        stream_reader = dctx.stream_reader(f)
        text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')
        df = pd.read_csv(text_stream)
    return df

class LocalPuzzleDatabase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.puzzles = self.load_puzzles()

    def load_puzzles(self):
        df = read_zst_csv(self.file_path)
        return df

    def get_random_puzzle(self):
        puzzle = self.puzzles.sample(1).iloc[0]
        fen = puzzle['FEN']
        moves = puzzle['Moves'].split()
        return fen, moves
