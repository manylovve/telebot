import telebot
import datetime
from telebot import types
import sqlite3
import schedule
import time
bot = telebot.TeleBot('6246891997:AAFOY9LwrQ7on7qcUww8I5WxDXJScp9pqc8')


# Function to create a new database connection
def create_connection():
    conn = sqlite3.connect('subscriptions.db')
    return conn


# Function to create a new cursor object
def create_cursor(conn):
    return conn.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напиши /help', parse_mode='html')


@bot.message_handler()
def get_user_text(message):
    conn = create_connection()
    cursor = create_cursor(conn)

    nums = int(datetime.datetime.utcnow().isocalendar()[1])
    dt = datetime.datetime.now().strftime('%d.%m.%Y')
    if (nums % 2) == 0:
        NED = 'знаменатель'
    else:
        NED = 'числитель'

    if NED == 'знаменатель':
        if message.text == "Какая неделя":
            bot.send_message(message.chat.id, NED, parse_mode='html')
        elif message.text == "Подписаться":
            subscribe(message, cursor, conn)
        elif message.text == "Отписаться":
            unsubscribe(message, cursor, conn)
        elif message.text == "/help":
            help(message)
        elif message.text == "Понедельник":
            photo = open('понедельник з.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == "Вторник":
            photo = open('вторник.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == "Среда":
            bot.send_message(message.chat.id, 'выходной')
        elif message.text == "Четверг":
            photo = open('четверг з.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == "Пятница":
            bot.send_message(message.chat.id, 'выходной')
        elif message.text == "Суббота":
            photo = open('суббота.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        else:
            bot.send_message(message.chat.id, 'кринж', parse_mode='html')
    else:
        if message.text == "Какая неделя":
            bot.send_message(message.chat.id, NED, parse_mode='html')
        elif message.text == "Подписаться":
            subscribe(message, cursor, conn)
        elif message.text == "Отписаться":
            unsubscribe(message, cursor, conn)
        elif message.text == "/help":
            help(message)
        elif message.text == "Понедельник":
            photo = open('понедельник ч.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == "Вторник":
            photo = open('вторник.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == "Среда":
            photo = open('среда ч.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == "Четверг":
            photo = open('четверг ч.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == "Пятница":
            bot.send_message(message.chat.id, 'выходной')
        elif message.text == "Суббота":
            photo = open('суббота.png', 'rb')
            bot.send_photo(message.chat.id, photo)

    cursor.close()
    conn.close()


@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    nedel = types.KeyboardButton('Какая неделя')
    pon = types.KeyboardButton('Понедельник')
    vtor = types.KeyboardButton('Вторник')
    sred = types.KeyboardButton('Среда')
    chet = types.KeyboardButton('Четверг')
    pyat = types.KeyboardButton('Пятница')
    sub = types.KeyboardButton('Суббота')
    subscribe_btn = types.KeyboardButton('Подписаться')
    unsubscribe_btn = types.KeyboardButton('Отписаться')

    markup.add(nedel, pon, vtor, sred, chet, pyat, sub, subscribe_btn, unsubscribe_btn)
    bot.send_message(message.chat.id,
                     'нажимаешь на день недели и получаешь расписание в зависимости от типа недели, bot created by manylovv66',
                     reply_markup=markup)


@bot.message_handler(commands=['subscribe'])
def subscribe(message, cursor, conn):
    chat_id = message.chat.id
    # Check if the chat_id already exists in the database
    cursor.execute("SELECT * FROM subscribers WHERE chat_id=?", (chat_id,))
    if cursor.fetchone() is None:
        # If chat_id doesn't exist, insert it into the database
        cursor.execute("INSERT INTO subscribers (chat_id) VALUES (?)", (chat_id,))
        conn.commit()
        bot.send_message(chat_id, "Вы подписались на рассылку.")
    else:
        bot.send_message(chat_id, "Вы уже подписаны на рассылку.")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message, cursor, conn):
    chat_id = message.chat.id
    cursor.execute("DELETE FROM subscribers WHERE chat_id=?", (chat_id,))
    conn.commit()
    bot.send_message(chat_id, "Вы отписались от рассылки.")


def send_broadcast_message(text):
    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("SELECT chat_id FROM subscribers")
    subscribers = cursor.fetchall()
    for subscriber in subscribers:
        bot.send_message(subscriber[0], text)
    cursor.close()
    conn.close()


# Schedule job to send message
schedule.every().day.at("14:39").do(send_broadcast_message, text="Не забудь про пары!")

# Start bot polling
while True:
    schedule.run_pending()
    time.sleep(1)
