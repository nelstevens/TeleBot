import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CallbackContext, CommandHandler
from telegram.ext import filters
# import from local scripts
from weather import get_weather, location_handler, weather_start, weather_conv_handler
from bus import bus_start
from trivia import trivia_conv_handler
# get environment variable from dotenv file
load_dotenv()

# load necessary env variable
TELEGRAM_API_TOKEN = os.getenv('TG_API_TOK')


# Start-Befehl
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        """Hallo! Sende mir einen Befehl (/...), damit ich dir helfen kann.\n
        Folgende Befehele sind möglich:\n
        /weather: Dieser Befehl zeigt dir diverse Wetterdaten für deinen Standort an.\n
        /bus: Dieser Befehl zeigt dir die nächsten Busabfahrten für Breitloo und TBD.\n
        /trivia: Dieser Befehl stellt dir ein Rätsel. Antworte mit der korrekten Zahl.
        """
        
    )

# Hauptfunktion
def main():
    # Neue Initialisierung mit Application für Version 20+
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # start
    application.add_handler(CommandHandler("start", start))
    # Handlers for weather
    application.add_handler(weather_conv_handler)
    # Handler for bus
    application.add_handler(CommandHandler('bus', bus_start))
    # Handlers for trivia
    application.add_handler(trivia_conv_handler)
    # Bot starten
    application.run_polling()

if __name__ == '__main__':
    main()
