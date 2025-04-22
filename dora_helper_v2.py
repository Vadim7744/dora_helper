import telebot
from telebot import types

BOT_TOKEN = "7500382014:AAGSAJ33hpruX5cZ8hldyCSRKEKQsWCtOSI"
bot = telebot.TeleBot(BOT_TOKEN)

# Функция для создания клавиатуры с кнопками "Ввести заново" и "Сброс ввода"
def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_restart = types.KeyboardButton('Сброс ввода')
    keyboard.add(button_restart)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Старт')
    keyboard.add(button_start)
    bot.send_message(message.chat.id, "Привет! Вас приветствует помощник Dora. Нажмите кнопку 'Старт' для начала.", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Старт')
def start_calculation(message):
    bot.send_message(message.chat.id, "Введите возраст в формате (лет:месяцев):", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    if message.text == 'Сброс ввода':
        start(message)
        return
    age = message.text
    try:
        years, months = map(int, age.split(':'))
        if years < 0 or months < 0:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "❗❗Неверный формат данных❗❗. Введите возраст в формате (лет:месяцев) еще раз:", reply_markup=create_keyboard())
        bot.register_next_step_handler(message, get_age)
        return
    bot.send_message(message.chat.id, "Введите рост (см):", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, get_height)

def get_height(message):
    global height
    if message.text == 'Сброс ввода':
        start(message)
        return
    try:
        height = float(message.text) / 100  # Переводим см в метры
    except ValueError:
        bot.send_message(message.chat.id, "❗❗Неверный формат данных❗❗. Введите рост (см) еще раз:", reply_markup=create_keyboard())
        bot.register_next_step_handler(message, get_height)
        return
    bot.send_message(message.chat.id, "Введите вес (кг):", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, get_weight)

def get_weight(message):
    global weight
    if message.text == 'Сброс ввода':
        start(message)
        return
    try:
        weight = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "❗❗Неверный формат данных❗❗. Введите вес (кг) еще раз:", reply_markup=create_keyboard())
        bot.register_next_step_handler(message, get_weight)
        return
    bot.send_message(message.chat.id, "Введите значение жировой массы:", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, get_fat_mass)

def get_fat_mass(message):
    global fat_mass
    if message.text == 'Сброс ввода':
        start(message)
        return
    try:
        fat_mass = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "❗❗Неверный формат данных❗❗. Введите значение жировой массы еще раз:", reply_markup=create_keyboard())
        bot.register_next_step_handler(message, get_fat_mass)
        return
    bot.send_message(message.chat.id, "Введите значение скелетно-мышечной массы:", reply_markup=create_keyboard())
    bot.register_next_step_handler(message, get_muscle_mass)

def get_muscle_mass(message):
    global muscle_mass
    if message.text == 'Сброс ввода':
        start(message)
        return
    try:
        muscle_mass = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "❗❗Неверный формат данных❗❗. Введите значение скелетно-мышечной массы еще раз:", reply_markup=create_keyboard())
        bot.register_next_step_handler(message, get_muscle_mass)
        return
    calculate_and_send_result(message)

def calculate_and_send_result(message):
    # Расчет ИМТ
    bmi = weight / (height ** 2)
    bot.send_message(message.chat.id, f"ИМТ = {bmi:.2f}")
    # Оценка рисков развития иППР
    if 7.2 <= fat_mass <= 13.6 and 13.6 <= muscle_mass <= 17.6:
        bot.send_message(message.chat.id, "Ожирение в составе синдрома иППР. Высокий риск развития иППР")
    elif 18.4 <= fat_mass <= 25.5 and 10.4 <= muscle_mass <= 14.1:
        bot.send_message(message.chat.id, "Ожирение как самостоятельное заболевание. Низкий риск развития иППР")
    else:
        bot.send_message(message.chat.id, "Ожирение отсутствует. Низкий риск развития иППР")

@bot.message_handler(func=lambda message: message.text == 'Сброс ввода')
def handle_reset(message):
    start(message)
bot.polling(none_stop=True)