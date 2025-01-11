import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
# import from local script
from weather import get_weather, location_handler, weather_start
# get environment variable from dotenv file
load_dotenv()

# load necessary env variable
TELEGRAM_API_TOKEN = os.getenv('TG_API_TOK')


# Start-Befehl
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hallo! Sende mir einen Befehl (/...), damit ich dir helfen kann")

# Hauptfunktion
def main():
    # Neue Initialisierung mit Application für Version 20+
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # start
    application.add_handler(CommandHandler("start", start))
    # Handlers for weather
    application.add_handler(CommandHandler("weather", weather_start))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))
    # Bot starten
    application.run_polling()

if __name__ == '__main__':
    main()
