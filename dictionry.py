import telebot
from telebot import types
import json
from difflib import get_close_matches

token = ''

bot = telebot.TeleBot(token)


def newmarcup():
    marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/new')
    item2 = types.KeyboardButton('/del')
    marcup.add(item1, item2)
    return marcup


@bot.message_handler(commands=["start"])
def start(message):
    marcup = newmarcup()
    bot.send_message(message.chat.id, "привет", reply_markup=marcup)
    stiker = open("hello", "rb")
    bot.send_sticker(message.chat.id, stiker)


@bot.message_handler(commands=["del"])
def new_word(message):
    msg = bot.send_message(message.chat.id, 'напишите слова или значение которое нужно удалить')
    bot.register_next_step_handler(msg, delet)


def delet(message):
    with open("file.json", "r") as file:
        data = json.load(file)
        with open("file.json", "w") as file:
            words = message.text.lower().split()
            for value in words:
                if value in data:
                    del[data[value]]
                elif value in list(data.values()):
                    delword = list(data.values()).index(value)
                    word = list(data.keys())[delword]
                    del[data[word]]
                else:
                    msg = bot.send_message(message.chat.id, "нет такого слова")
                    bot.register_next_step_handler(msg, delet)
            json.dump(data, file, indent=4)


@bot.message_handler(commands=["new"])
def new_word(message):
    marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('❌break❌')
    marcup.add(item1)
    msg = bot.send_message(message.chat.id, """
напишите в форме:
'слова-значение'
'слова-значение'...
отмена - нажмите '❌break❌'""", reply_markup=marcup)
    MessageID = message.id
    bot.register_next_step_handler(msg, Save)
    return MessageID


def Save(message):
    words = message.text.lower().split('\n')
    if message.text == "❌break❌":
        marcup = newmarcup()
        bot.send_message(message.chat.id, "закончили", reply_markup=marcup)
    elif not texteror(words):
        msg = bot.send_message(message.chat.id, """
напишите в форме:
'слова-значение'
'слова-значение'...
отмена - нажмите '❌break❌'""")
        bot.register_next_step_handler(msg, Save)
    elif texteror(words):
        print(2)
        with open("file.json", "r") as file:
            data = json.load(file)
        with open("file.json", "w") as file:
            for values in words:
                word = values.split("-")
                data[word[0]] = word[1]
            json.dump(data, file, indent=4)
            marcup = newmarcup()
            bot.send_message(message.chat.id, 'сохранили', reply_markup=marcup)

#обработака ошибок
def texteror(text):
    for word in text:
        if "-" not in word:
            print(1)
            print(6)
            return False
            break
        word = word.split('-')
        if word[0][-1] == ' ' or word[1][0] == ' ':
            print(3)
            print(word[0][-1])
            return False
            break
    else:
        print('else')
        return True




@bot.message_handler(content_types=["text"])
def send_message(message):
        with open('file.json', 'r') as file:
            data = json.load(file)
        if message.text.lower() in data:
            word = f"{message.text} - {data[message.text.lower()]}"
            bot.send_message(message.chat.id, word)
        elif message.text.lower() in data.values():
            words = list(data.values())
            word = list(data.keys())[words.index(message.text.lower())]
            bot.send_message(message.chat.id, f"{message.text} - {word}")
        elif len(get_close_matches(message.text.lower(), data.keys())) > 0:
            marcup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item = types.KeyboardButton('yes')
            item2 = types.KeyboardButton('no')
            marcup.add(item, item2)
            bot.send_message(message.chat.id, f'возможна вы имели ввиду {get_close_matches(message.text.lower(), data.keys())[0]}',reply_markup=marcup)
        else:
            bot.send_message(message.chat.id, 'Нет такого слова')





bot.polling()
