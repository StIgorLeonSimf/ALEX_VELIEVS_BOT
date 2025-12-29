import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (Message, CallbackQuery as TgCallbackQuery,
                           LabeledPrice, ContentType, InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           PreCheckoutQuery as TgPreCheckoutQuery)
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio

from config import TOKEN, PAYMENTS_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
VIDEO_FILES = {
    'video_1': {'path': 'video1.mp4', 'price': 50000},
    'video_2': {'path': 'video2.mp4', 'price': 100000},
}


class BuyCallback(CallbackData, prefix='buy'):
    video_id: str  # buy: video_1


@dp.message(Command('start'))
async def start_handler(message: Message):
    kbd = InlineKeyboardBuilder()
    for k, v in VIDEO_FILES.items():
        kbd.button(text=f'Купить видео {v["path"]}',
                   callback_data=BuyCallback(video_id=k))
    kbd.adjust(1)
    await message.answer('Выбирайте', reply_markup=kbd.as_markup())


@dp.callback_query(BuyCallback.filter())
async def buy_callback_handler(callback: TgCallbackQuery, callback_data: BuyCallback):
    video = VIDEO_FILES.get(callback_data.video_id)

    if not video:
        await callback.message.answer("Файл не найден!")
        return
    price = LabeledPrice(label=f"Video {callback_data.video_id}", amount=video["price"])
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"Покупка видео {callback_data.video_id}",
        description=f"Стоимость {video['price'] // 100} rub.",
        payload=callback_data.video_id,
        provider_token=PAYMENTS_TOKEN,
        currency="RUB",
        prices=[price],
        start_parameter=f"purchase-{callback_data.video_id}"
    )
    await callback.answer()


@dp.pre_checkout_query()  # подтверждение платежа
async def pre_checkout_handler(pre_checkout_q: TgPreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    video_id = message.successful_payment.invoice_payload
    video_info = VIDEO_FILES.get(video_id)
    if not video_info:
        await message.answer('ошибка - видео не найдено')
        return
    # отправляем файл
    with open(video_info['path'], 'rb') as video_file:
        await message.answer_video(video_file,
                                   caption=f'Спасибо за покупку {video_id}')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

# from dataclasses import dataclass
#
#
# class Car:
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return f'Car(name=\'{self.name}\')'
#
#     def __eq__(self, other):
#         return self.name == other.name
#
# @dataclass
# class Car1:
#     name: str
#     model = '2410'
#
# car = Car('Volga')
# car2 = Car('volga')
# print(car == car2)
# car1 = Car1('Gaz')
# car11 = Car1('Gaz')
# print(car1)
# print(car1 == car11)
