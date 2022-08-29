
from dataclasses import dataclass
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import json 
import random as rd
from googletrans import Translator

import os
from dotenv import load_dotenv
load_dotenv('.env')

TOKEN = os.getenv('TOKEN')


#from translate import Translator
#translator= Translator(from_lang="english",to_lang="spanish")

translator = Translator(service_urls=['translate.googleapis.com'])

updater = Updater(TOKEN, use_context=True)

def getData():
    with open('quote.json') as file:
        data = json.load(file)
    return data

def getRandomQuote(data):
    length = len(data['quotes'])
    l = rd.randint(0,length)
    return (data['quotes'][l]['quote'])

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    username = update.message.chat.first_name
    update.message.reply_text(
		f"Hola {username} 🤗, Bienvenido al bot de las frases del Dr House bot. Recuerda que todos mienten ")
    update.message.reply_text(f"Hi {username} 🤗 Welcome to Dr House quotes. Remenber Everybody lies")
    update.message.reply_text("new quote | nueva frase /quote")
    update.message.reply_text("help | ayuda /help")


def quote(update: Update, context: CallbackContext):
    data = getData()
    q = getRandomQuote(data)
    q = "".join(q)
    translation = translator.translate(q, dest='es')
    update.message.reply_text(q)
    #print(translation.text)
    update.message.reply_text(translation.text)

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /github - To get the source code URL
    /quote - To get Dr House Quote""")

def github(update: Update, context: CallbackContext):
     update.message.reply_text(
        "github URL => https://github.com/edwight-delgado/dr_house_quote_telegram-bot")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)
  
  
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
  
def main():
    PORT = int(os.environ.get('PORT','8443'))
    HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('quote', quote))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.command, unknown))  # Filters out unknown commands
    
    # Filters out unknown messages.
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
    
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path= TOKEN,
		      webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
    
    updater.idle()

if __name__ == '__main__':
    main()
