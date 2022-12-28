from telebot import TeleBot, types
import os
import operation as op
import logger as lg
import urllib.request

TOKEN = ' ' # Ввести токен

bot = TeleBot(TOKEN)

dct = {}


@bot.message_handler(commands=['start', 'help'])
def welcome_answer(msg: types.Message):
    bot.send_message(chat_id=msg.from_user.id, text=f'Здравствуйте, {msg.from_user.first_name}!\nВас приветствует Записная книга - "Книжок" ver.0.1.\n'
                    'Для продолжения работы введите /menu')
    lg.Log('Programm has been started') 


@bot.message_handler(commands=['log'])
def send_log(msg: types.Message):
    bot.register_next_step_handler(msg, send_log(msg))
    lg.Log('User has been selected log') 


name_it = ''
surname_it = ''
number_it = ''
description_it = ''


@bot.message_handler(content_types=['text', 'document'])
def menu(message):
    if message.text == '/menu':
        bot.send_message(message.chat.id, f'Выберите необходимый пункт меню, введя соответствующую команду: \n/1 - Добавить новую позицию.\n'
        '/2 - Вывести записную книгу на экран.\n/3 - Импорт из файла.\n/4 - Экспорт в файл.\n')

    elif message.text == '/1':
        lg.Log('The user has selected item number 1')
        bot.send_message(message.chat.id, 'Введите Имя')
        bot.register_next_step_handler(message, get_name)

    elif message.text == '/2':
        lg.Log('The user has selected item number 2')        
        bot.send_message(message.chat.id, op.Print_csv())
        bot.send_message(message.chat.id, f'Введите /menu для возврата в меню')

    elif message.text == '/3':
        lg.Log('The user has selected item number 3') 
        bot.send_message(message.chat.id, f'Выберите необходимый формат: \n/31 - Разделитель строка.\n/32 - Разделитель точка с запятой')
        
    elif message.text == '/31':
        lg.Log('The user has selected item number 31') 
        bot.send_message(message.chat.id, f'Введите файл')    
        bot.register_next_step_handler(message, get_file_txt)
        
    elif message.text == '/32':
        lg.Log('The user has selected item number 32') 
        bot.send_message(message.chat.id, f'Введите файл')    
        bot.register_next_step_handler(message, get_file_csv)

    elif message.text == '/4':
        lg.Log('The user has selected item number 4') 
        bot.send_message(message.chat.id, 'Выберите необходимый формат: \n/41 - Разделитель строка.\n/42 - Разделитель точка с запятой')

    elif message.text == '/41':
        lg.Log('The user has selected item number 41') 
        bot.send_message(message.chat.id, f'Введите имя файла')
        bot.register_next_step_handler(message, send_txt)

    elif message.text == '/42':
        lg.Log('The user has selected item number 42') 
        bot.send_message(message.chat.id, f'Введите имя файла')
        bot.register_next_step_handler(message, send_csv)

    else:
        lg.Log('The user has selected error') 
        bot.send_message(message.chat.id, f'Я Вас не понимаю. Введиnt: /help.')


def get_name(message):
    global name_it
    name_it = message.text
    lg.Log('User entered: {name_it}')
    bot.send_message(message.chat.id, f'Введите фамилию')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname_it
    surname_it = message.text
    lg.Log('User entered: {surname_it}')
    bot.send_message(message.chat.id, f'Введите номер телефона')
    bot.register_next_step_handler(message, get_number)


def get_number(message):
    global number_it
    number_it = message.text
    lg.Log('User entered: {number_it}')
    bot.send_message(message.chat.id, f'Введите описание')
    bot.register_next_step_handler(message, get_description)


def get_description(message):
    global description_it
    description_it = message.text
    lg.Log('User entered: {description_it}')
    op.Create(name_it, surname_it, number_it, description_it)
    bot.send_message(message.chat.id, f'Контакт успешно добавлен!\nВведите /menu для возврата в меню')


def get_file_txt(msg: types.Message):
    filename = msg.document.file_name
    with open(filename, 'wb') as file:
        file.write(bot.download_file(bot.get_file(msg.document.file_id).file_path))
    lg.Log('Import file has created') 
    op.Import_txt(filename)
    bot.send_message(chat_id=msg.from_user.id, text=f'{filename} Файл успешно принят и загружен в базу!\nВведите /menu для возврата в меню')
    lg.Log('Import file is included in the database') 


def get_file_csv(msg: types.Message):
    filename = msg.document.file_name
    with open(filename, 'wb') as file:
        file.write(bot.download_file(bot.get_file(msg.document.file_id).file_path))
    lg.Log('Import file has created') 
    op.Import_csv(filename)
    bot.send_message(chat_id=msg.from_user.id, text=f'{filename} Файл успешно принят и загружен в базу!\nВведите /menu для возврата в меню')
    lg.Log('Import file is included in the database') 


def send_txt(message):
    filename = message.text
    print(filename)
    op.Export_txt(filename)
    file = open(filename, 'rb')
    bot.send_document(message.chat.id, file)
    bot.send_message(message.chat.id, text=f'Файл успешно отправлен!\nВведите /menu для возврата в меню')
    lg.Log('Export file has been sent') 


def send_csv(message):
    filename = message.text
    op.Export_csv(filename)
    file = open(filename, 'rb')
    bot.send_document(message.chat.id, file)
    bot.send_message(message.chat.id, text=f'Файл успешно отправлен!\nВведите /menu для возврата в меню')
    lg.Log('Export file has been sent') 


def send_log(message):
    file = open('log.csv', 'rb')
    bot.send_document(message.chat.id, file)
    bot.send_message(message.chat.id, text=f'Файл с логами успешно отправлен!\nВведите /menu для возврата в меню')
    lg.Log('log file has been sent') 


print('server start')
bot.infinity_polling()