import asyncio
from function_processing import get_trush_table, get_sdnf
from telebot.async_telebot import AsyncTeleBot
from token_file import token
from telebot import types
from prettytable import PrettyTable

bot = AsyncTeleBot(token)

buttons = {"doc": "Показать документацию"}
start_keyboard = types.ReplyKeyboardMarkup()
start_keyboard.add(buttons['doc'])


@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет это парсер логических выражений. Давайте построим таблицу истинности и СДНФ', reply_markup=start_keyboard)


@bot.message_handler(commands=['get_data'])
async def get_data(message):
    args = message.text.split()[1:]
    variables = sorted(args[0].split(','))
    expression = args[1]
    table, vector = get_trush_table(expression, variables)
    table_to_view = PrettyTable(variables + ['F'])
    table_to_view.add_rows(table)
    try:
        await bot.send_message(message.chat.id,
                                f"""```txt\nТаблица истинности для функции {expression}\n
                                        {table_to_view.get_string()}\n\n{vector}\n\n
                                        {get_sdnf(table, variables)}\n```""",
                                  parse_mode='MarkdownV2')
    except IndexError:
        await bot.reply_to(message, "Неверный формат выражения!")


@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    if message.text == buttons['doc']:
        document = open('about.txt', 'rb')
        await bot.send_document(message.from_user.id, document)


if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True))