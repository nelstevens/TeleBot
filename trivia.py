import random
import os
import requests
import logging
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# set sequence
ASK = range(1)

corectAnswer = 0

def get_question():
    url = 'https://opentdb.com/api.php?amount=1'
    logger.info(url)
    response = requests.get(url)
    logger.info(response)
    if response.status_code == 200:
        data = response.json()['results'][0]
        cor = data['correct_answer']
        nst = [data['incorrect_answers'], [cor]]
        unest = [k for i in nst for k in i]
        opts = random.sample(unest, len(unest))
        # get index of correct value and set as global variable
        global correctAnswer
        correctAnswer = opts.index(cor)
        out = {
            'Que': data['question'],
            'Opt': opts,
            'Cor': cor
        }
    return out

def format_question(dat):
    return f"{dat['Que']}\n\n\n" + "\n".join(f"{index + 1}. {item}" for index, item in enumerate(dat['Opt'])) + "\n\n\n reply with the corrext number."

def ask_question():
    dat = get_question()
    stri = format_question(dat)
    return stri

# Start-Befehl
async def trivia_start(update: Update, context: CallbackContext):
    await update.message.reply_text(ask_question())

    return ASK

# fun for checking answer
async def checkanswer_handler(update: Update, context: CallbackContext):
    logger.info(update.message.text)
    logger.info(correctAnswer)
    if update.message.text:
        # if correct say correct else say false
        if int(update.message.text) == correctAnswer + 1:
            await update.message.reply_text("Correct!")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Wrong! try again!")
            return ASK
    

# set cancel handler
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Bye!")

    return ConversationHandler.END

# create conversation Handler
trivia_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("trivia", trivia_start)],
    states={
        ASK: [MessageHandler(filters.TEXT, checkanswer_handler)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)