import telebot

from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

bot.delete_webhook()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет! Я бот секретарь с искусственным интеллектом")


@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.send_message(message.from_user.id, 'Я вас не понимаю(')


bot.infinity_polling()
