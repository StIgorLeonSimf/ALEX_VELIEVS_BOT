import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message, FSInputFile
from config import TOKEN

from mistralai import Mistral
from pydantic import BaseModel
from instructor import from_mistral, Mode
from docxtpl import DocxTemplate

api_key = 'PlmCfQ0UxbjbQo2eHHTCw4CRxhSCDbn9'
model = 'mistral-large-latest'


class MessageInfo(BaseModel):
    city: str
    name: str
    description: str


def fill_the_doc(city, name, description):
    tpl = DocxTemplate('template.docx')
    context = {
        'city': city,
        'name': name,
        'description': description
    }
    tpl.render(context)
    tpl.save('result.docx')


logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

client = Mistral(api_key=api_key)
instructor_client = from_mistral(client=client, mode=Mode.MISTRAL_TOOLS)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Привет, я бесплатный ИИ бот!!!')


@dp.message(F.text)
async def filter_messages(message: Message):
    ai_response = instructor_client.chat.completions.create(
        response_model=MessageInfo,
        model=model,
        messages=[
            {"role": "user", "content": message.text, }
        ],
        temperature=0,
    )
    print(ai_response)
    fill_the_doc(ai_response.city, ai_response.name, ai_response.description)
    doc = FSInputFile('result.docx', filename='Письмо.docx')
    await message.answer_document(document=doc,
                                  caption='Ваш сгенерированный док')


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


# print(ai_response.choices[0].message.content)
if __name__ == '__main__':
    asyncio.run(main())
