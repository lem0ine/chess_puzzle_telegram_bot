from config import TELEGRAM_TOKEN
from telegram_api import TelegramAPI
from chess_bot import ChessBot
from local_puzzle_database import LocalPuzzleDatabase
from file_utils import download_file

def main():
    url = "https://database.lichess.org/lichess_db_puzzle.csv.zst"
    local_filename = "lichess_db_puzzle.csv.zst"
    download_file(url, local_filename)
    telegram_api = TelegramAPI(TELEGRAM_TOKEN)
    puzzle_database = LocalPuzzleDatabase("lichess_db_puzzle.csv.zst")
    chess_bot = ChessBot(telegram_api, puzzle_database)
    chess_bot.start_bot()

if __name__ == '__main__':
    main()
