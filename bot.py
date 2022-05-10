import telegram
import logging
import random
import math

from telegram import *
from telegram.ext import *

def start(update: Update, context: CallbackContext):
    global data, game_start, letter
    for text_line in ['Welcome to the City Word Chain game!'+
        '\nThe rules are simple: we are naming cities in turns.'+
        '\nEach city must start with the same letter the city previously said ends with.'+
        '\nExample: LondoN - New YorK - KarachI',
        'You can stop the game by typing /stop.',
        'Cities Database (c) 2022 Simplemaps.com: simplemaps.com/data/world-cities']:
        context.bot.send_message(chat_id=update.effective_chat.id, \
                             text=text_line)
    game_start = True
    load_data()
    randletter = random.randint(0, 25)
    randcity = dist_rand(len(data[randletter]))
    context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='My turn: ' + data[randletter][randcity][0] + \
                             '\nYour letter: ' + chr(define_letter(data[randletter][randcity][1]) + ord('A')))
    letter = define_letter(data[randletter][randcity][1])

def stop(update: Update, context: CallbackContext):
    global game_start
    context.bot.send_message(chat_id=update.effective_chat.id, \
                text='You can start a new game by typing /start.')
    game_start = False

def dist_rand(upperbound):
    rand = random.randint(0, min(upperbound-1, 40))
    if rand >= upperbound: rand = upperbound - 1
    return rand

def define_letter(city):
    for i in range(len(city)-1, -1, -1):
        ltr = city[i].upper()
        if ord(ltr) >= ord('A') and ord(ltr) <= ord('Z'):
            return ord(ltr) - ord('A')
    return 0

def turn(update: Update, context: CallbackContext):
    global game_start, data, letter, repeats
    if not game_start:
        context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='You can start a game by typing /start.')
        return
    else:
        city = update.message.text[0].upper() + update.message.text[1:]
        start_ltr = ord(city[0]) - ord('A')
        if start_ltr < 0 or start_ltr > 25:
            context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='Type the name of a city!')
            return
        if start_ltr != letter:
            context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='Your city must start with letter ' + chr(letter + ord('A')) + '!')
            return
        if city in repeats:
            context.bot.send_message(chat_id=update.effective_chat.id, \
                text='This city has already been named')
            return
        has_city = False
        city_raw = []
        for c in data[letter]:
            if c[1] == city or c[0] == city:
                has_city = True
                city_raw = c
                break
        if not has_city:
            context.bot.send_message(chat_id=update.effective_chat.id, \
                text='Sorry, we don\'t know about a city named ' + city + \
                '\nPlease connect to the developer if there\'s a city not included in my database.')
            return
        repeats.append(city)
        data[letter].remove(city_raw)
        letter = define_letter(city)
        if len(data[letter]) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='Hmmmmm...\n...\n...\nWellll...\n...\n...\n...\nI give up! You\'ve defeated me!')
            context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='You can start a new game by typing /start.')
            game_start = False
            return
        randcity = dist_rand(len(data[letter]))
        context.bot.send_message(chat_id=update.effective_chat.id, \
                                 text='Your turn: ' + city_raw[0] + '\nMy turn: ' + data[letter][randcity][0] + \
                                 '\nYour letter: ' + chr(define_letter(data[letter][randcity][1]) + ord('A')))
        letter = define_letter(data[letter][randcity][1])

def load_data():
    global data
    data = []
    repeats = []
    for i in range(26):
        data.append([])
    with open('data/worldcities.csv', mode='r', encoding='utf8') as data_file:
        lines = data_file.readlines()[1:]
        for line in lines:
            _city = line.replace('"','').split(',')
            start_ltr = _city[1][0]
            start_id = 0
            for ltr in _city[1][0]:
                if (ord(ltr) >= ord('A') and ord(ltr) <= ord('Z')) or \
                   (ord(ltr) >= ord('a') and ord(ltr) <= ord('z')):
                    start_ltr = ltr
                    break
                start_id += 1
            _city[1] = _city[1][start_id].upper() + _city[1][start_id+1:]
            try:
                if [_city[0], _city[1]] not in data[ord(_city[1][0].upper())-ord('A')]:
                    data[ord(_city[1][0].upper())-ord('A')].append([_city[0], _city[1]])
            except Exception as E:
                print(E)
                print(_city[1])
                exit()

game_start = False
letter = 0
data = []
repeats = []
load_data()
updater = Updater(token='5335852405:AAFRdrLS3Je67wSBtqwlI2b4061yrWBmXAU', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)
game_handler = MessageHandler(Filters.text, turn)
dispatcher.add_handler(game_handler)

updater.start_polling()
