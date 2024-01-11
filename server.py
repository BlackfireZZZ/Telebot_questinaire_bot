import telebot
from telebot import types
from data import Questions
import json
token = "put your token here"


bot = telebot.TeleBot(token)
# ось x - выгорания пользователя
# ось y - лентяйства пользователя
xy_data = {}
counter_data = {}     # счётчик номера вопроса
data = {}


@bot.message_handler(commands=['start'])
def start(message):
    global xy_data, counter_data, data
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}! '
                                      f'Я протестирую, какой ты программист!\n'
                                      f'Информация о ваших предыдущих ответах не сохраняется.')
    # Здороваемся с пользователем по его нику в tg
    data[message.chat.id] = [-1] * len(Questions().texts)
    counter_data[message.chat.id] = 0
    xy_data[message.chat.id] = [0, 0]
    ask_question(message)


def ask_question(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создаем кнопки для выбора опции
    option1 = types.KeyboardButton("1")
    option2 = types.KeyboardButton("2")
    option3 = types.KeyboardButton("3")
    option4 = types.KeyboardButton("4")
    option5 = types.KeyboardButton("/stop")
    option6 = types.KeyboardButton("Start again")
    keyboard.add(option1, option2, option3, option4, option5, option6)
    print(counter_data[message.chat.id])
    text = Questions().texts[counter_data[message.chat.id]]
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def get_result(message):
    id = message.chat.id
    if xy_data[id][0] == 0 and xy_data[id][1] == 0:
        bot.send_message(id, "Надо вырабатывать хоть какие-нибудь черты характера?\n"
                                          "Пока что их определить невозможно..")
    elif xy_data[id][0] >= 0 and xy_data[id][1] >= 0:
        bot.send_message(id, "Ты выгоревший лентяй. Вообще с дивана вставал?")
        bot.send_photo(id, open('lazy_man.jpg', 'rb'), caption="Вот как тебя видит Шедеврум!")
    elif xy_data[id][0] >= 0 and xy_data[id][1] < 0:
        bot.send_message(id, "Ты выгоревший трудяга. Найди себе интересный проект для души и всё будет ок) \n"
                                          "Ну или тупо отдохни недельку..")
        bot.send_photo(id, open('tired_man.jpg', 'rb'), caption="Вот как тебя видит Шедеврум!")
    elif xy_data[id][0] < 0 and xy_data[id][1] >= 0:
        bot.send_message(id, "Ты интересующийся лентяй. Твой удел - читать статейки с дивана!")
        bot.send_photo(id, open('lazy_interested_man.jpg', 'rb'), caption="Вот как тебя видит Шедеврум!")
    elif xy_data[id][0] < 0 and xy_data[id][1] < 0:
        bot.send_message(id, "Ты работяга! Респект!")
        bot.send_photo(id, open('interested_man.jpg', 'rb'), caption="Вот как тебя видит Шедеврум!")
    with open('data.json', 'w') as f:
        json.dump(data, f)


@bot.message_handler(content_types=['text'])
def check_answer(message):
    global xy_data, counter_data, data

    id = message.chat.id
    print(counter_data[id], xy_data[id], message.text)
    if message.text == "1":  # Во всех вопросах ответ под определённым номером дает один и тот же результат
        xy_data[id][0] -= 1
        xy_data[id][1] -= 1
        data[id][counter_data[id]] = int(message.text)
    elif message.text == "2":
        xy_data[id][0] += 1
        xy_data[id][1] -= 1
        data[id][counter_data[id]] = int(message.text)
    elif message.text == "3":
        xy_data[id][0] -= 1
        xy_data[id][1] += 1
        data[id][counter_data[id]] = int(message.text)
    elif message.text == "4":
        xy_data[id][0] += 1
        xy_data[id][1] += 1
        data[id][counter_data[id]] = int(message.text)
    elif message.text == "/stop":
        bot.send_message(id, "Bye, " + message.from_user.first_name + "!")
    elif message.text == "Start again":
        start(message)
    else:
        bot.send_message(id, "Такой опции нет, попробуй снова!")
        ask_question(message)

    counter_data[id] += 1
    if counter_data[id] == len(Questions().texts):
        get_result(message)
    else:
        ask_question(message)





bot.polling(none_stop=True, interval=0)