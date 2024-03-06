from telethon import TelegramClient
from typing import Awaitable, Optional, List
from telethon.tl.types import Message, User, Channel
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
import logging

logging.basicConfig(level=logging.INFO)


class TelegramAPI:
    def __init__(self, api_id: int, api_hash: str) -> None:
        """
        Инициализирует объект TelegramAPI.

        :param api_id: Идентификатор API приложения Telegram.
        :param api_hash: Хэш API приложения Telegram.
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient('session', api_id, api_hash)

    async def auth(self) -> None:
        """
        Выполняет процесс авторизации в Telegram.

        При необходимости запрашивает пароль для сеанса или корректный код подтверждения телефона.
        """
        try:
            await self.client.start()
            logging.info('Авторизация в Телеграм успешна')
        except SessionPasswordNeededError:
            logging.warning('Необходим облачный пароль')
            password = input("Введите пароль для сеанса: ")
            await self.client.start(password=password)
        except PhoneCodeInvalidError:
            logging.error('Неверный код авторизации')
            code = input("Введите корректный код подтверждения телефона: ")
            await self.client.sign_in(code=code)

    async def get_messages(self, chat_id: int) -> List[Message]:
        """
        Получает список сообщений из указанного чата.

        :param chat_id: Идентификатор чата.
        :return: Список объектов Message, представляющих сообщения в чате.
        """
        try:
            id_of_last_message_in_chat = await self._get_id_of_last_message(chat_id)
            return await self.client.get_messages(chat_id, min_id=0, max_id=id_of_last_message_in_chat)
        except Exception as e:
            logging.error(f"Ошибка при получении сообщений: {e}")
            return []

    async def _get_id_of_last_message(self, chat_id: int) -> Optional[int]:
        """
        Возвращает идентификатор последнего сообщения в указанном чате.

        :param chat_id: Идентификатор чата.
        :return: Идентификатор последнего сообщения или None, если чат пуст.
        """
        try:
            last_message_from_chat = await self.client.get_messages(chat_id)
            if last_message_from_chat:
                last_message_data = last_message_from_chat[0]
                message_id = last_message_data.id
                return int(message_id)
            else:
                return None
        except Exception as e:
            logging.error(f"Ошибка при получении последнего сообщения: {e}")
            return None
        except IndexError:
            logging.error('Получен пустой список сообщений для поиска последнего ID')
            message_id = 1
            return message_id

    async def get_channel_data_from_link(self, telegram_chat_link: str) -> Channel:
        """
        Получает данные о канале по указанной ссылке.

        :param telegram_chat_link: Ссылка на канал.
        :return: Объект Channel, представляющий данные о канале.
        """
        try:
            return await self.client.get_entity(telegram_chat_link)
        except Exception as e:
            logging.error(f"Ошибка при получении данных канала: {e}")

    async def get_users(self, chat_id: int) -> List[User]:
        """
        Получает список пользователей в указанном чате.

        :param chat_id: Идентификатор чата.
        :return: Список объектов User, представляющих пользователей в чате.
        """
        try:
            data = await self.client.get_participants(chat_id)
            return data
        except Exception as e:
            logging.error(f"Ошибка при получении пользователей: {e}")
            return []

    async def stop(self) -> None:
        """
        Останавливает клиент TelegramClient.
        """
        try:
            await self.client.disconnect()
        except Exception as e:
            logging.error(f"Ошибка при остановке клиента: {e}")
