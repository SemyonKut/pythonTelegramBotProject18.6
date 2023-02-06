import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)


# START информация о работе бота.
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = '🤖\n' \
           'Бот производит конвертацию валют.\n\n' \
           'Для начала работы введите команду в формате:\n' \
           '<название исходной валюты> <в какую валюту перевести> <сумма исходной валюты>\n' \
           'Посмотреть список доступных валют: /values\n' \
           'Просмотр информации о работе бота: /help\n'
    bot.reply_to(message, text)


# HELP информация о работе бота.
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = '📖\n' \
           'Для начала работы введите команду в формате:\n' \
           '<название исходной валюты> <в какую валюту перевести> <сумма исходной валюты>\n' \
           'Посмотреть список доступных валют: /values'
    bot.reply_to(message, text)


# VALUES список доступных валют.
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '¤\n' \
           'Доступные валюты:'
    for key in keys.keys():
        text = '\n *'.join((text, key))
    bot.reply_to(message, text)


# CONVERT обработчик перевода валют.
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise ConvertionException('Необходимо ввести 3 параметра')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n*** {e} ***')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n*** {e} ***')
    else:
        text = f'Цена {amount} {keys[quote]} = {total_base} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()

'''

# тест
@bot.message_handler()
def echo(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Hi')
    
     *base_ticker = keys[base]
    
     *none_stop=True
'''


