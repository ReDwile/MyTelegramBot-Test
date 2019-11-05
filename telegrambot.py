import telebot
from telebot import types

first_name = '' #Имя
last_name = '' #Фамилия
username = ''
id_user = '' 
users = [] #Будут храниться id юзеров, которые активировали бота хотя бы один раз

#Добавить токен своего бота
token = ''
bot = telebot.TeleBot(f'{token}')
@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    if message.text == '/start':
        keyboard = types.InlineKeyboardMarkup() #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
        keyboard.add(key_yes) #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.from_user.id, text='Хочешь узнать, что известно боту, когда ты взаимодействуешь с ним?', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global first_name
    global last_name
    global username
    global id_user

    first_name = call.from_user.first_name
    if type(first_name) != str:
        first_name = 'У тебя это скрыто'
    last_name = call.from_user.last_name
    if type(last_name) != str:
        last_name = 'У тебя это скрыто'
    username = call.from_user.username
    if type(username) != str:
        username = 'У тебя это скрыто'
    id_user = call.from_user.id
    if type(id_user) != int:
        id_user = 'У тебя это скрыто'

    string = 'Твое имя: ' + first_name + '\nТвоя фамилия: ' + last_name + '\nТвой id: ' + str(id_user) + '\nТвой ник в телеге: ' + username + '\n'

    if not id_user in users:
        print(string) #Выводит информацию каждого пользователя, который активировал бота (выводит не более одного раза)
        users.append(id_user)

    if call.data == "yes":

        if len(first_name) != 0:
            bot.send_message(call.message.chat.id, string + 'Аккуратнее. Общайся только с проверенными ботами.')
        else:
            bot.send_message(call.message.chat.id, 'Упс... Произошла ошибочка\nНапиши /start еще раз')

    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Жаль. Кто знает, может эта инфа тебе поможет воздержаться от сообщения левому боту.')

    first_name = ''
    last_name = ''
    username = ''
    id_user = ''

bot.polling(none_stop=True, interval=0)