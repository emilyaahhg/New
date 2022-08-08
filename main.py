import pygsheets
from email import message
import telebot
from telebot import types
from datetime import datetime

# Pygsheet
service_file = r'C:\Users\Emily\Desktop\timer\cvsuproj-925460f8f3be.json'
gc = pygsheets.authorize(service_file=service_file)
sheetname = 'InternTimeLogger'
sh = gc.open(sheetname)
wks = sh.worksheet_by_title('test')
wks2 = sh.worksheet_by_title('masterlist')

# Telegram API Token
API_TOKEN = '5554859250:AAHsL3LmPZsYt1tQHKFnJCESIISAzY1OP-4'
bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User:
    def __init__(self, name):
        self.timein = name
        self.timeout = None

print("Getting Started...")

# Start
@bot.message_handler(commands=['start'])
def process_start(message):
    username = message.chat.username
    finduser = wks2.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        bot.reply_to(message, """
Hi! Interns I am your TimeLoggerBot.\n
type /timein - login
type /timeout - logout
type /details - details
""")

# Help
@bot.message_handler(commands=['help'])
def process_help(message):
    username = message.chat.username
    finduser = wks2.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        bot.reply_to(message, "Available Commands: \n\n/timein\n/timeout\n/details\n")
    
# Timein
@bot.message_handler(commands=['timein'])   
def process_timein(message):
    username = message.chat.username
    finduser = wks2.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now = datetime.now()
            date_time = now.strftime("%H:%M:%S")
            time = now.strftime("%H:%M:%S")
            date = now.strftime('%m/%d/%y')
            chat_id = message.chat.id
            timein = message.text
            user = User(timein)
            user_dict[chat_id] = user
            user.timein = date_time
            
            if timein == "/timein":
                user_first_name = str(message.chat.first_name)
                user_last_name = str(message.chat.last_name)
                fullname = user_first_name + " "+ user_last_name
                grecord = wks.get_all_records()
                num = 2
                for i in range(len(grecord)):
                    num+=1
                    if fullname == grecord[i].get("Name") and date == grecord[i].get("Date"):
                        bot.reply_to(message, f'You have already timed in')
                        break
                else:
                    wks.update_value((num, 1), fullname)
                    wks.update_value((num, 2), date)
                    wks.update_value((num, 3), time)
                    
                    bot.reply_to(message, f'Successfully timein on {str(date_time)}')

        except Exception as e:
            bot.reply_to(message, 'There was an error, please try again.')
    else:
        bot.reply_to(message, 'Only registered Nexlogic interns can use this bot')

 
# Timeout
@bot.message_handler(commands=['timeout'])  
def process_timeout(message):
    username = message.chat.username
    finduser = wks2.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        try:
            now2 = datetime.now()
            date_time2 = now2.strftime("%H:%M:%S")
            time = now2.strftime("%H:%M:%S")
            timeout = message.text 
            user = User(timeout)
            user.timeout = date_time2
            user_first_name = str(message.chat.first_name)
            user_last_name = str(message.chat.last_name)
            fullname = user_first_name + " "+ user_last_name
            
            date = now2.strftime('%m/%d/%y')

            if timeout == "/timeout":
                grecord = wks.get_all_records()
                num = 1
                for i in range(len(grecord)):
                    num += 1
                    if fullname == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timeout")== '':
                        wks.update_value((num,4),time)
                        bot.reply_to(message, f'Successfully timeout on {str(date_time2)}')
                        break
                    elif fullname == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timeout")!= '':
                        bot.reply_to(message, 'You have already timed out')

        except Exception as e:
            bot.reply_to(message, 'There was an error, please try again.')
    else:
        bot.reply_to(message, 'Only registered Nexlogic interns can use this bot')


# Status
@bot.message_handler(commands=['details'])  
def process_details(message):
    username = message.chat.username
    finduser = wks2.find(username)
    nofind = int(len(finduser))
    if nofind >= 1:
        user_first_name = str(message.chat.first_name) 
        user_last_name = str(message.chat.last_name)
        fullname = user_first_name + " "+ user_last_name
        now = datetime.now()
        date = now.strftime('%m/%d/%y')
        grecord = wks.get_all_records()
        num = 1
        for i in range(len(grecord)):
            num += 1
            if fullname == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")!= '':
                bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: {grecord[i].get("Timeout")}')
                break
            elif fullname == grecord[i].get("Name") and date == grecord[i].get("Date") and grecord[i].get("Timein")!= '' and grecord[i].get("Timeout")== '':
                bot.reply_to(message, f'Date {date}\nTimein: {grecord[i].get("Timein")}\nTimeout: NONE')
                break
        else:
            bot.reply_to(message, "You haven't TIMED IN yet today")
    else:
        bot.reply_to(message, 'Only registered Nexlogic interns can use this bot')
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
