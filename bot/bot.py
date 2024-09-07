import telebot
from telebot import types
from config import BOT_TOKEN
from auth.auth import authenticate_user, register_user
bot = telebot.TeleBot(BOT_TOKEN)

bot.delete_webhook()

commands = [
        types.BotCommand(command="/start", description="Начать работу"),
        types.BotCommand(command="/help", description="Информационное сообщение"),
    ]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def send_welcome(message):

    markup1 = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup_item1 = telebot.types.InlineKeyboardButton('Войти', callback_data='Sign in')
    markup_item2 = telebot.types.InlineKeyboardButton('Зарегистрироваться', callback_data='Log in')
    markup1.add(markup_item1, markup_item2)

    bot.send_message(message.from_user.id, "Привет! Я бот секретарь с искусственным интеллектом", reply_markup=markup1)



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
        if call.data == 'func1' or call.data == 'func2' or call.data == 'func3':
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
        if call.data == 'Sign in':
            mes = bot.send_message(call.message.chat.id, 'Введите:\nЛогин\nПароль')
            bot.register_next_step_handler(mes, sign_in)

        if call.data == 'Log in':
            mes = bot.send_message(call.message.chat.id, 'Зарегистрируйте:\nЛогин\nПароль')
            bot.register_next_step_handler(mes, log_in)

def sign_in(message):
    try:
        email = message.text.split('\n')[0]
        password = message.text.split('\n')[1]
        user_id = message.from_user.id
        authenticate_user(user_id, email, password)
        bot.send_message(message.from_user.id, 'Успешный вход')

    except Exception:
        bot.send_message(message.from_user.id, 'Некорректный ввод')


def log_in(message):
    try:
        email = message.text.split('\n')[0]
        password = message.text.split('\n')[1]
        user_id = message.from_user.id
        register_user(user_id, email, password)
        bot.send_message(message.from_user.id, 'Успешная регистрация')

    except Exception:
        bot.send_message(message.from_user.id, 'Некорректный ввод')


# def audio_file(message):
    # bot.send_audio(message.from_user.id, audio=open('audio.mp3', 'rb'))


@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.send_message(message.from_user.id, 'Я вас не понимаю(')


if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)



