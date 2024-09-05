import telebot

bot = telebot.TeleBot("7192984868:AAHBpPgmYktWhIRx0plDLvL8OB0krVuDAVc")

bot.delete_webhook()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет! Я бот секретарь с искусственным интеллектом")


@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.send_message(message.from_user.id, 'Я вас не понимаю(')


bot.infinity_polling()
