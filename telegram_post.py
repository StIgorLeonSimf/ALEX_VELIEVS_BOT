from config import TOKEN, CHANNEL_ID

import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from mistralai import Mistral

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()
api_key = 'PlmCfQ0UxbjbQo2eHHTCw4CRxhSCDbn9'
model = 'mistral-large-latest'
client = Mistral(api_key=api_key)

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    channel_id = CHANNEL_ID
    while True:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    'role': 'system',
                    'content': 'Ты ведешь Телеграм канал. '
                               'Пиши посты о том, что просит пользователь '
                               'без лишней информации.'
                },
                {
                    'role': 'user',
                    'content': 'Напиши шутку про музыкантов.'
                }
            ]
        )
        await bot.send_message(channel_id,
                               chat_response.choices[0].message.content,
                               parse_mode="Markdown")
        await asyncio.sleep(15)


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())