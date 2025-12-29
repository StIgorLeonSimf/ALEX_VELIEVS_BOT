from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.database.request as rq
import app.keyboard as kb

router = Router()


class Reg(StatesGroup):
    name = State()
    age = State()
    number = State()


@router.message(Command('reg'))
async def name(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите имя: ')


@router.message(Reg.name)
async def name_age(message, state):
    await state.update_data(name=message.text)
    await state.set_state(Reg.age)
    await message.answer('Введите возраст: ')


@router.message(Reg.age)
async def age_number(message, state):
    await state.update_data(age=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите ТЛФ: ', reply_markup=kb.get_number)


# @router.message(Reg.number)
# async def number(message, state):
#     await state.update_data(number=message.text)
#     data = await state.get_data()
#     await message.answer(f'Cпасибо за регистрацию\n'
#                          f'Имя: {data["name"]} \n'
#                          f'Возраст: {data["age"]}\n'
#                          f'ТЛФ: {data["number"]}')
#     await state.clear()

@router.message(Reg.number, F.contact)
async def number(message, state):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Cпасибо за регистрацию\n'
                         f'Имя: {data["name"]} \n'
                         f'Возраст: {data["age"]}\n'
                         f'ТЛФ: {data["number"]}')
    await state.clear()


@router.message(Command('get_photo1'))
async def get_photo(message):
    await message.answer_photo(
        photo='https://st3.depositphotos.com/3994509/34477/'
              'i/380/depositphotos_344777646-stock-photo-'
              'liquid-nitrogen-show-for-kids.jpg',

        caption='Здесь делаем подпись')

@router.message(Command('get_photoAmi'))
async def get_photo(message):
    await message.answer_photo(
        # photo='AgACAgIAAxkBAAMkaQRgdoZOEu-F1Gidl431wiXTO2MAAkD'
        #       '-MRti-yhI8vuL6H6IJ1MBAAMCAAN5AAM2BA',

        photo='AgACAgIAAxkBAAIBFWlI494eTqXe1a1HxwtZ4gZXEIILAAJSEms'
              'bTOFISsVsD60JotK7AQADAgADeAADNgQ',
        caption='Здесь делаем подпись')


@router.message(F.photo)
async def get_photo(message):
    await message.answer(f'ID photo: {message.photo[-1].file_id}')


@router.message(F.text == 'Как дела?')
async def how_are_you(message):
    await message.answer('Все здорово!')


@router.message(F.text == 'Как тебя зовут?')
async def my_name(message):
    await message.answer('My name is Alex')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(f'Start - начать работу\n'
                         f'help - получить подсказки\n'
                         f'get_photo - получить картинку')


# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.reply(f'Привет.\n'
#                         f'Твой ID: {message.from_user.id}\n'
#                         f'Имя: {message.from_user.first_name}',
#                         reply_markup=kb.main)




@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию',
                         reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Выбрана категория')
    await callback.message.answer('Выберите товар',
                                  reply_markup=await kb.items(
                                      callback.data.split('_')[1]
                                  ))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Выбран товар')
    await callback.message.answer(f'Название: {item_data.name}\n'
                                  f'Описание: {item_data.description}\n'
                                  f'Цена: {item_data.price} $',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))


# @router.callback_query(F.data == 'sneakers')
# async def sneakers(callback: CallbackQuery):
#     await callback.answer('Кроссовки', show_alert=True)
#     await callback.message.answer('Выбраны кроссовки')
@router.callback_query(F.data == 'sneakers')
async def sneakers(callback: CallbackQuery):
    await callback.answer('Кроссовки', show_alert=True)
    await callback.message.edit_text('Выбраны кроссовки',
                                     reply_markup=await kb.inline_cars())


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'Добро пожаловать в магазин кроссовок',
                         reply_markup=kb.main)