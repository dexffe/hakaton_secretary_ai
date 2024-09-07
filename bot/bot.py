import telebot
from telebot import types
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

bot.delete_webhook()

commands = [
        types.BotCommand(command="/start", description="Начать работу"),
        types.BotCommand(command="/help", description="Информационное сообщение"),
    ]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет! Я бот секретарь с искусственным интеллектом")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    text = 'Здравствуйте!\nДанный бот предназначен для  для создания протоколов совещаний и генерации их расшифровки.\n\n*Расшифровка совещания* позволяет получить в текстовом формате запись совещаний.\n\n*Официальный протокол* включает в себя: дату, время, перечень присутствующих, деление на основные блоки, ключевые предложения, контекст обсуждения каждого предложения, время в аудиозаписи, протокол поручений (кому поручено, контекст поручения, срок выполнения).\n\n*Неофициальный протокол* включает в себя: дату, время, длительность, участников (опционально), повестку дня (опционально), деление на основные блоки, контекст обсуждения каждого предложения (опционально),время в аудиозаписи.'
    bot.send_message(message.from_user.id, text, parse_mode='Markdown')




def chek_markup(func1:bool, func2:bool, func3:bool) -> types.InlineKeyboardMarkup:
    global FUNC1, FUNC2, FUNC3        # необходимые глобальные переменные(чтобы их видел callback_inline()) для проверки состояния чекбоксов
    FUNC1, FUNC2, FUNC3 = func1, func2, func3

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)       # создание пустого markup

    text_func1 = 'func1: ✅' if func1 else 'func1: ⬜'
    text_func2 = 'func2: ✅' if func2 else 'func2: ⬜'            # проверка, какой чекбокс включен, а какой нет
    text_func3 = 'func3: ✅' if func3 else 'func3: ⬜'

    markup_item1 = telebot.types.InlineKeyboardButton(text_func1, callback_data='func1')
    markup_item2 = telebot.types.InlineKeyboardButton(text_func2, callback_data='func2') # создание верного чекбокс(вкл/выкл)
    markup_item3 = telebot.types.InlineKeyboardButton(text_func3, callback_data='func3')

    markup.add(markup_item1, markup_item2, markup_item3)

    return markup


@bot.message_handler(commands=["text"])
def default_test(message):
    bot.send_message(message.chat.id,
                     text="Выберите необходимые функции:",
                     reply_markup=chek_markup(func1=False, func2=False, func3=False))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'func1':
            markup = chek_markup(not FUNC1, FUNC2, FUNC3)   # изменение состояния чекбокса (№ 1)
        elif call.data == 'func2':
            markup = chek_markup(FUNC1, not FUNC2, FUNC3)   # изменение состояния чекбокса (№ 2)
        elif call.data == 'func3':
            markup = chek_markup(FUNC1, FUNC2, not FUNC3)   # изменение состояния чекбокса (№ 3)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Выберите необходимые функции:",
                              reply_markup=markup)




@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.send_message(message.from_user.id, 'Я вас не понимаю(')


if __name__ == '__main__':
    bot.polling(none_stop=True)



