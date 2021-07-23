

import time
import telebot
from telebot import types

TOKEN = '1848688988:AAFywkuspJlhUlSDdWb6tZZEFwWBBddscd8'

knownUsers = [] 
userStep = {} 

commands = {  
    'start'       : 'Iniciar bot',
    'help'        : 'Ayuda',
}

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
imageSelect.add('Grados Celsius a Grados Kelvin ', 'Grados Kelvin a Grados Celsius')

hideBoard = types.ReplyKeyboardRemove()  

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("Nuevo usuario detectadp pero uso otro comando y no \"/start\"")
        return 0



def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Solo estos comandos estan disponibles\n\n"
    for key in commands: 
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text) 

@bot.message_handler(commands=['start'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Elija una opcion: ", reply_markup=imageSelect) 
    userStep[cid] = 1  


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    bot.send_chat_action(cid, 'typing')

    if text == 'Grados Celsius a Grados Kelvin':  
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "A continuacíon se le mostrará la formula")
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(5)   
        bot.send_photo(cid, open('celsius_a_kelvin.png', 'rb'),
                       reply_markup=hideBoard)
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "Espero haberte ayudado, usa /start para realzar otra consulta o /help para comandos disponibles")
        userStep[cid] = 0

    elif text == 'Grados Kelvin a Grados Celsius':
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "A continuacíon se le mostrará la formula")
        bot.send_chat_action(cid, 'upload_photo')
        time.sleep(5)   
        bot.send_photo(cid, open('kelvin_a_celsius.png', 'rb'),
                       reply_markup=hideBoard)
        bot.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, "Espero haberte ayudado, usa /start para realizar otra consulta o /help para comnandos disponibles")
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Please, use the predefined keyboard!")
        bot.send_message(cid, "Please try again")




@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):

    bot.send_message(m.chat.id, "No entiendo la palabra \"" + m.text + "\"\nUsa /start para usar el bot")


bot.polling()