import telegram
import logging
import random
import math

from telegram import *
from telegram.ext import *

def start(update: Update, context: CallbackContext):
    for text_line in ['Welcome to the City Word Chain game!',
        'The rules are simple: we are naming cities in turns.',
        'Every city must start with the same letter the city previously said ends with.',
        'Example: LondoN - New YorK - KarachI',
        'You can stop the game by typing /stop.',
        'Cities Database (c) 2022 Simplemaps.com: simplemaps.com/data/world-cities']:
        context.bot.send_message(chat_id=update.effective_chat.id, \
                             text=text_line)
    game_start = True
    randcity = round((1-math.cos(random.random()*math.pi/2)))*len(data)
    if randcity >= len(data): randcity = len(data) - 1
    context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='My turn: ' + data[randcity][0] + \
                             '\nYour letter: ' + data[randcity][1][-1].upper())

def turn(update: Update, context: CallbackContext):
    if not game_start:
        context.bot.send_message(chat_id=update.effective_chat.id, \
                             text='You can start a game by typing /start.')
        return
    
    
data = []
with open('data/worldcities.csv', mode='r', encoding='utf8') as data_file:
    lines = data_file.readlines()[1:]
    for line in lines:
        city = line.replace('"','').split(',')
        data.append([city[0], city[1], True])

updater = Updater(token='5128904056:AAFOCO-KanniggJh164eCYat2EzVEEP32I0', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
game_handler = MessageHandler(Filters.text, turn)
dispatcher.add_handler(game_handler)

game_start = False
letter = '-'

updater.start_polling()
