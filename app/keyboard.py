from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.request import get_categories, get_category_item


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton
                     (text=category.name,
                      callback_data=f'category_{category.id}'))
    keyboard.add(InlineKeyboardButton
                 (text='На главную',
                  callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name,
                                          callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную',
                                      callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Информация'), KeyboardButton(text='Контакты'),
     KeyboardButton(text='детализация')]
], resize_keyboard=True, input_field_placeholder='Приглашение ввода')

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Study', url='https://www.youtube.com/channel/UCYnx9DWM7kiEzTcIOvbsYBA')]
])

# catalog = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='кепка', callback_data='cap')],
#     [InlineKeyboardButton(text='кроссовки', callback_data='sneakers')],
#     [InlineKeyboardButton(text='куртка', callback_data='t-short')],
# ])

get_number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить номер ТЛФ', request_contact=True)]
], resize_keyboard=True)

cars = {'Mercedes': 'https://www.youtube.com/channel/UCYnx9DWM7kiEzTcIOvbsYBA',
        'BMW': 'https://www.youtube.com/channel/UCYnx9DWM7kiEzTcIOvbsYBA',
        'Toyota': 'https://www.youtube.com/channel/UCYnx9DWM7kiEzTcIOvbsYBA',
        'Volga': 'https://www.youtube.com/channel/UCYnx9DWM7kiEzTcIOvbsYBA'}


# async def reply_cars():
#     keyboard = ReplyKeyboardBuilder()
#     for car in cars:
#         keyboard.add(KeyboardButton(text=car))
#     return keyboard.adjust(2).as_markup()


async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car, target in cars.items:
        keyboard.add(InlineKeyboardButton(text=car, url=target))
    return keyboard.adjust(2).as_markup()
