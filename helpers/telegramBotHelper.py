from asyncio import sleep

import telegram
from telegram.error import TimedOut, BadRequest, RetryAfter, Unauthorized, NetworkError


class TelegramBotHelper:

    def __init__(self):
        self.bot = telegram.Bot(token='5411025218:AAH0Daj8Dm0QpShAQDTCt3i9pfjz8Th2SNU')

    def get_updates(self, object_index):
        # you can find chat id by opening https://api.telegram.org/bot+token/getUpdates in browser
        # chat with me: 248932976
        # chat with group: -1001362475026
        updates = self.bot.get_updates()[object_index].message.chat_id
        return updates

    def send_photo(self, chat_id: int, photo):
        self.bot.send_photo(chat_id, photo)

    def send_message(self, chat_id: int, message):
        try:
            self.bot.sendMessage(chat_id=chat_id, text=message)
        except BadRequest as e:
            self.bot.sendMessage(chat_id=chat_id, text=message)
        except RetryAfter as e:
            sleep(5)
            self.bot.sendMessage(chat_id=chat_id, text=message)
        except TimedOut as e:
            sleep(5)
            self.bot.sendMessage(chat_id=chat_id, text=message)
        except Unauthorized as e:
            sleep(0.25)
        except NetworkError as e:
            sleep(5)
            self.bot.sendMessage(chat_id=chat_id, text=message)
        except Exception as e:
            sleep(1)
            self.bot.sendMessage(chat_id=chat_id, text=message)