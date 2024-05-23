import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramAPI:
    def __init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}/"

    def send_message(self, chat_id, message, parse_mode=None):
        url = f"{self.base_url}sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}
        response = requests.post(url, data=data)
        if response.status_code != 200:
            logger.error(f"Failed to send message to {chat_id}: {response.status_code}")

    def send_photo(self, chat_id, photo, caption=None):
        url = f"{self.base_url}sendPhoto"
        files = {"photo": ("chess_board.png", photo, "image/png")}
        data = {"chat_id": chat_id, "caption": caption}
        response = requests.post(url, files=files, data=data)
        if response.status_code != 200:
            logger.error(f"Failed to send photo to {chat_id}: {response.status_code}")

    def receive_updates(self, offset=None):
        url = f"{self.base_url}getUpdates?timeout=100"
        if offset:
            url += f"&offset={offset}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['result']
        else:
            logger.error(f"Failed to get updates: {response.status_code}")
            return None
