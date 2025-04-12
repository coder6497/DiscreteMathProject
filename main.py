import asyncio
from function_processing import get_trush_table, get_sdnf, trush_table
from telebot.async_telebot import AsyncTeleBot
from token_file import token
from telebot import types

bot = AsyncTeleBot(token)

buttons = {"doc": "Показать документацию"}
start_keyboard = types.ReplyKeyboardMarkup()
start_keyboard.add(buttons['doc'])


@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет это парсер логических выражение? Давайте построим таблицу истинности и СДНФ', reply_markup=start_keyboard)


@bot.message_handler(commands=['get_data'])
async def get_data(message):
    get_data_keyboard = types.ReplyKeyboardMarkup()
    args = message.text.split()[1:]
    variables = sorted(args[0].split(','))
    expression = args[1]
    get_data_keyboard.add('/start')
    await bot.reply_to(message, get_trush_table(expression, variables))
    await bot.send_message(message.chat.id, get_sdnf(variables), reply_markup=get_data_keyboard)
    trush_table.clear()


@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    if message.text == buttons['doc']:
        document = open('about.txt', 'rb')
        await bot.send_document(message.from_user.id, document)


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True))