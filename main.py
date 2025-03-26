import threading
import time
from datetime import datetime
import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
token=os.getenv('TOKEN') #чтобы не искать потом 7044459383:AAGE-K-UOkT-gZocdJ6tXGb4rk7VNYpH4BM
bot=telebot.TeleBot(token)

def default_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_add = types.KeyboardButton('Добавить')
    btn_del = types.KeyboardButton('Удалить')
    btn_done = types.KeyboardButton('Отметить выполненным')
    btn_view = types.KeyboardButton('Просмотреть задачи')
    markup.add(btn_add, btn_del,btn_done,btn_view)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет ✌️ ", reply_markup=default_markup())

@bot.message_handler(func= lambda x:  x.text=='Добавить')
def add_task(message):
    markup = types.ReplyKeyboardMarkup()
    btn_undo = types.KeyboardButton('Отмена')
    markup.add(btn_undo)
    msg=bot.send_message(message.chat.id,"Напиши название задачи", reply_markup=markup)
    bot.register_next_step_handler(msg, task_name)

def task_name(message):
    name = message.text
    if name == 'Отмена':
        bot.send_message(message.chat.id, "Добавление задачи отменено", reply_markup=default_markup())
        return
    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.KeyboardButton('Домашка')
    btn_2 = types.KeyboardButton('Кружки')
    btn_3 = types.KeyboardButton('Личное')
    btn_undo = types.KeyboardButton('Отмена')
    markup.add(btn_1, btn_2, btn_3, btn_undo)
    msg=bot.send_message(message.chat.id,"В какую категорию добавить?", reply_markup=markup)
    bot.register_next_step_handler(msg, task_type, name)

def task_type(message, name):
    type_ = message.text
    if type_ == 'Отмена':
        bot.send_message(message.chat.id, "Добавление задачи отменено", reply_markup=default_markup())
        return
    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.KeyboardButton('Да')
    btn_2 = types.KeyboardButton('Нет')
    btn_undo = types.KeyboardButton('Отмена')
    markup.add(btn_1, btn_2, btn_undo)
    msg=bot.send_message(message.chat.id,"Это важное?", reply_markup=markup)
    bot.register_next_step_handler(msg, task_priority, name, type_)

def task_priority(message, name, type_):
    priority = message.text
    if priority == 'Отмена':
        bot.send_message(message.chat.id, "Добавление задачи отменено", reply_markup=default_markup())
        return
    markup = types.ReplyKeyboardMarkup()
    btn_undo = types.KeyboardButton('Отмена')
    markup.add(btn_undo)
    msg=bot.send_message(message.chat.id,"Каков дедлайн? (Мы предупредим вас за час до него) Напишите 'нет', чтобы создать задачу без дедлайна.", reply_markup=markup)
    bot.register_next_step_handler(msg, task_deadline, name, type_, priority)

def task_deadline(message, name, type_, priority):
    deadline = message.text
    if deadline == 'Отмена':
        bot.send_message(message.chat.id, "Добавление задачи отменено", reply_markup=default_markup())
        return
    # добавление в датабазу
    bot.send_message(message.chat.id, "Готово!", reply_markup=default_markup())

def deadline_thread():
    while 1:
        time.sleep(120)

#threading.Thread(target=deadline_thread, daemon=True).start()

@bot.message_handler(func= lambda x:  x.text=='Удалить')
def del_task(message):
    markup = types.ReplyKeyboardMarkup()
    btn_undo = types.KeyboardButton('Отмена')
    markup.add(btn_undo)
    msg=bot.send_message(message.chat.id,"Напиши название задачи", reply_markup=markup)
    bot.register_next_step_handler(msg, task_name2)

def task_name2(message):
    name = message.text
    if name == 'Отмена':
        bot.send_message(message.chat.id, "Удаление задачи отменено", reply_markup=default_markup())
        return
    msg = bot.send_message(message.chat.id, "Удалено", reply_markup=default_markup())

@bot.message_handler(func= lambda x:  x.text=='Отметить выполненным')
def del_task(message):
    markup = types.ReplyKeyboardMarkup()
    btn_undo = types.KeyboardButton('Отмена')
    markup.add(btn_undo)
    msg=bot.send_message(message.chat.id,"Напиши название задачи", reply_markup=markup)
    bot.register_next_step_handler(msg, task_name3)

def task_name3(message):
    name = message.text
    if name == 'Отмена':
        bot.send_message(message.chat.id, "Выполнение фунции отменено", reply_markup=default_markup())
        return
    msg = bot.send_message(message.chat.id, "Задача отмечена как выполненная", reply_markup=default_markup())



bot.infinity_polling()
