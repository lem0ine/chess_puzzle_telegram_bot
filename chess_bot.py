import logging
from chess_puzzle import ChessPuzzle
from local_puzzle_database import LocalPuzzleDatabase
from telegram_api import TelegramAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChessBot:
    def __init__(self, telegram_api, puzzle_database):
        self.telegram_api = telegram_api
        self.puzzle_database = puzzle_database
        self.current_puzzle = {}
        self.modes = {}
        self.flag = 0

    def start_bot(self):
        offset = None
        while True:
            updates = self.telegram_api.receive_updates(offset)
            if updates:
                for update in updates:
                    message = update.get("message")
                    if message:
                        text = message.get("text")
                        chat_id = message["chat"]["id"]
                        user_id = message["from"]["id"]
                        if user_id not in self.modes:
                            self.modes[user_id] = 'auto'  # Установка режима по умолчанию при первом взаимодействии
                        self.process_message(chat_id, user_id, text)
                        offset = update["update_id"] + 1

    def send_puzzle(self, user_id):
        if user_id in self.current_puzzle:
            self.telegram_api.send_message(user_id, "У вас уже есть текущая задача. Решите её или используйте команду /reset для сброса.")
        else:
            fen, moves = self.puzzle_database.get_random_puzzle()
            puzzle = ChessPuzzle(fen, moves)
            puzzle_image = puzzle.generate_puzzle()
            self.current_puzzle[user_id] = puzzle
            current_player = puzzle.get_current_player()
            self.telegram_api.send_photo(user_id, puzzle_image, f"Ваша задача готова! Ход {current_player}.")

    def process_message(self, chat_id, user_id, text):
        if text == "/start":
            welcome_message = (
                "Привет! Я бот для решения шахматных задач. Напишите /puzzle, чтобы получить новую задачу.\n"
                "Вы можете переключаться между автоматическим и слепым режимами с помощью команд /mode_auto и /mode_blind.\n"
                "В автоматическом режиме ходы оппонента будут делаться автоматически, после каждого из них вы будете получать \n"
                "доску с текущей позицией. \n"
                "В слепом режиме вы получаете только начальную позицию и должны вводить все ходы сам\n"
                "Напишите /help, чтобы посмотреть все команды"
            )
            self.telegram_api.send_message(chat_id, welcome_message)
        elif text == "/puzzle":
            self.send_puzzle(user_id)
        elif text == "/help":
            help_message = (
                "/start - Начать взаимодействие с ботом\n"
                "/puzzle - Получить новую шахматную задачу\n"
                "/instructions - Получить инструкцию по решению задач и использованию шахматной нотации\n"
                "/reset - Сбросить текущую задачу\n"
                "/help - Получить список команд\n"
                "/mode_auto - Включить автоматический режим\n"
                "/mode_blind - Включить слепой режим"
            )
            self.telegram_api.send_message(chat_id, help_message)
        elif text == "/instructions":
            instructions = (
                "Инструкция по решению шахматных задач:\n\n"
                "1. Получите шахматную задачу, используя команду /puzzle.\n"
                "2. Ваша задача - найти правильные ходы, чтобы выиграть.\n"
                "3. Вводите ходы в шахматной нотации. Например, 'e2e4' или 'Nf3'.\n"
                "4. Алгебраическая нотация ходов:\n"
                "   - Пешка: 'e4' (перемещение пешки на e4)\n"
                "   - Конь: 'Nf3' (перемещение коня на f3)\n"
                "   - Слон: 'Bf4' (перемещение слона на f4)\n"
                "   - Ладья: 'Rf1' (перемещение ладьи на f1)\n"
                "   - Ферзь: 'Qd3' (перемещение ферзя на d3)\n"
                "   - Король: 'Ke2' (перемещение короля на e2)\n"
                "   - Взятие: 'Nxf3' (конь берет фигуру на f3)\n"
                "Можно также использовать упрощенную нотацию, написав только начальную и конечную клетку фигуры, \n"
                "которой вы хотите сделать ход. Например, сдвинуть ладью с a1 на a8 с помощью команды a1a8."
                "5. Если ваш ход правильный, бот скажет вам продолжать.\n"
                "6. Если ваш ход неправильный, бот скажет вам попробовать снова.\n"
                "7. Если вы хотите сбросить задачу и начать новую, используйте команду /reset.\n\n"
                "Наслаждайтесь решением задач!"
            )
            self.telegram_api.send_message(chat_id, instructions)
        elif text == "/reset":
            if user_id in self.current_puzzle:
                del self.current_puzzle[user_id]
                self.telegram_api.send_message(chat_id, "Текущая задача сброшена.")
            else:
                self.telegram_api.send_message(chat_id, "У вас нет текущей задачи для сброса.")
        elif text == "/mode_auto":
            self.modes[user_id] = 'auto'
            self.telegram_api.send_message(chat_id, "Автоматический режим включен.")
        elif text == "/mode_blind":
            self.modes[user_id] = 'blind'
            self.telegram_api.send_message(chat_id, "Слепой режим включен.")
        else:
            self.check_user_move(chat_id, user_id, text)

    def check_user_move(self, chat_id, user_id, move):
        if user_id in self.current_puzzle:
            puzzle = self.current_puzzle[user_id]
            is_correct, feedback = puzzle.check_move(move)
            self.telegram_api.send_message(chat_id, feedback)
            if is_correct:
                if self.modes[user_id] == 'auto':
                    if not puzzle.solution_moves:
                        del self.current_puzzle[user_id]
                    else:
                        puzzle.make_opponent_move()
                        updated_board_image = puzzle.generate_puzzle()
                        self.telegram_api.send_photo(user_id, updated_board_image, "Ответный ход выполнен.")
                elif self.modes[user_id] == 'blind':
                    if not puzzle.solution_moves:
                        del self.current_puzzle[user_id]
        else:
            self.telegram_api.send_message(chat_id, "Для начала получите новую задачу командой /puzzle.")

    def send_feedback(self, user_id, feedback):
        self.telegram_api.send_message(user_id, feedback)
