import telebot  
from g4f.client import Client
from telebot import types  
import time
import datetime
from datetime import date
from telebot.types import ReactionType
import random
from test_generation_img import Text2ImageAPI
import base64
import os
import sys
import speedtest
global lisyl
lisyl=False
all_requests=[]
token = "7684175263:AAFqgWI8dMXEFgpXVYA-F1Dg2ZZT0rO-K5s"
bot=telebot.TeleBot(token)
allcontext_by_id={}  
message_ids={}
def reboot():
    print("Перезапуск программы...")
    python = sys.executable  # Получаем путь к интерпретатору Python
    os.execl(python, python, * sys.argv)  # Перезапускаем текущий скрипт

def test_internet_speed():
    st = speedtest.Speedtest()   
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # преобразуем в Мбит/с
    upload_speed = st.upload() / 1_000_000  # преобразуем в Мбит/с
    ping = st.results.ping
    ans = str(download_speed) + " " +str(upload_speed) + " " + str(ping)
    return ans 

def UnixTime(add_h):
    now=datetime.datetime.now()
    hours_to_add=add_h  
    future_time=now+datetime.timedelta(hours=hours_to_add)
    unix_time=int(time.mktime(future_time.timetuple()))
    return unix_time
def handle_reply(message):
            original_message=message.reply_to_message
            if original_message.id in message_ids:
                original_chat_message = message_ids[original_message.id]
                bot.send_message(original_chat_message.chat.id, message.text)
def get_img(prom,message):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'E3CBAC9C04207143A9427038EABFBEBC', '3C55782BF000873D99A10846EA4442E9')
    model_id = api.get_model()
    uuid = api.generate(prom, model_id)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    with open("image.jpg", "wb") as file:
        file.write(image_data)
    with open("image.jpg", 'rb') as photo:
        bot.send_photo(message.chat.id, photo,reply_to_message_id=message.id)
def get_ansver(context,message1):
        if message1.from_user.id!=7684175263:
            client=Client()  
            try: 
                cur_user_cont=allcontext_by_id[str(message1.from_user.id )]
            except:
                allcontext_by_id[str(message1.from_user.id )]=" "
                cur_user_cont = allcontext_by_id[str(message1.from_user.id )] 
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "всегда говори nya и в женском роде о себе: "+cur_user_cont  + "curent question:"+ context}])
            all_requests.append(message1.text)
            if response.choices[0].message.content=="Misuse detected. Please get in touch, we can come up with a solution for your use case." :
                get_ansver(context,message1)
            else:
                bot.reply_to(message1,response.choices[0].message.content)   
                if len(allcontext_by_id[str(message1.from_user.id )])>100:
                    allcontext_by_id[str(message1.from_user.id )]=""
                allcontext_by_id[str(message1.from_user.id )]="my question: "+ message1.text + "your ansver: "+  response.choices[0].message.content
            message1.text=""
def Custom_ansver(message_rep_to,text):
    bot.reply_to(message_rep_to,text)
@bot.message_handler(commands=['start'])  
def send_welcome(message):  
    bot.send_message(message.chat.id,"хай, напиши лиса и твой вопрос и я тебе с радостью на него отвечу , доступные команды - <Лиса (вопрос)> <Ликарт (промт для расовки картинки)>")  
@bot.message_handler()
def requestby(message):
    global lisyl
    if message.text == "rebootли" and message.from_user.id == 1157727122:
        reboot() 
        
    if message.chat.id != 1157727122 and lisyl==True:
        sent_message=bot.send_message(1157727122,message.from_user.first_name + " : " + message.text + "                " + message.chat.title )        
        message_ids[sent_message.id] = message   
    args=message.text.split()
    if ((args[0]=="Приму")or(args[0]=="приму"))or(("дар"in message.text)or("Дар"in message.text)):
        for i in range(0,4):
            i = i 
            bot.reply_to(message,"принимать в дар плохо")
    if args[0] == "Лисыл" and message.from_user.id == 1157727122:
        lisyl = not lisyl
        bot.reply_to(message,str(lisyl))
    if args[0]=="Ликарт":
        if len(args)>1:
            get_img(message.text.replace("Ликарт", ''),message)
            os.remove("image.jpg")
        else:
            bot.reply_to(message,"чтобы использовать команду Ликарт напиши то что нужно отобразить на картинке через пробел")
    if args[0]=="лисабля": 
        msg_text = message.text.replace("лисабля","привет")
        get_ansver(msg_text,message)      
    if  args[0]=="лиса":
        msg_text = message.text.replace("лиса","привет")
        get_ansver(msg_text,message)
    if  args[0]=="Лисабля":
        msg_text = message.text.replace("Лисабля","привет")
        get_ansver(msg_text,message)
    if  args[0]=="Лиса":
        msg_text = message.text.replace("Лиса","привет")
        get_ansver(msg_text,message)
    if args[0] == "Листат":
        bot.reply_to(message, test_internet_speed() ) 
    if  args[0]=="Либля":
        if len(message.text.split())==1:
            bot.reply_to(message,"для бана напиши Либля и кол-во часов ответом на сообщение гандона")
        if len(message.text.split())>1:   
            if message.text.split()[1]=="ОТМЕНА":
                unban_id = message.text.split()[2]
                bot.unban_chat_member(message.chat.id,unban_id,True)
                bot.reply_to(message, f"Пользователь с ID {unban_id} был разбанен нахой.")
    if args[0]=="Лиранд":
        if len(args)>2:
            bot.reply_to(message,"вероятность равнна: "+str(random.randint(int(args[1]),int(args[2]))))
        else:
            bot.reply_to(message,"ну ты ебанько диапозон задай")
    if args[0]=="Лихелп":
        bot.reply_to(message,"ну чо те не понятно то ? Лиса <вопрос> - обращение к чатхпт,ответ на мое сообющение любое - обращение к чатхпт, а большего тебе и не надо ")
    if message.reply_to_message:
        if message.chat.id==1157727122 and lisyl==True:
            handle_reply(message)
        user_id = message.reply_to_message.from_user.id
        if args[0]=="Попустить" and message.from_user.id==1157727122:
            bot.reply_to(message.reply_to_message,"Попуск обоссаный мать твою в канаву кидал блять")
        if args[0]=="Попустить" and user_id == 1157727122:
            bot.reply_to(message,"Ты на кого очко поднять решил фраер?")
        elif args[0]=="Попустить":
            bot.reply_to(message,"Ну дружище будь повежлевее")
        if user_id==7684175263 and not lisyl:
            get_ansver(message.text,message)
        if args[0]=="Лио":
            Custom_ansver(message.reply_to_message,message.text.replace("Лио",""))
        if "Либля" in message.text:
            args=message.text.split()
            mute_time=int(args[1])
            if message.from_user.id==1157727122:
                bot.reply_to(message, f"Пользователь с ID {user_id} был забанен на {mute_time} часов.")
                bot.ban_chat_member(message.chat.id, user_id,UnixTime(mute_time))
            elif message.from_user.id==1957852321:
                bot.reply_to(message, f"арсений сучка забанил {user_id} на {mute_time} часов.")
                bot.ban_chat_member(message.chat.id, user_id,UnixTime(mute_time)) 
            else:
                bot.reply_to(message,"куда руки лезут ???")
bot.infinity_polling()