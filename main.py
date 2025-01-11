import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram.ext import filters
# import from local script
from weather import get_weather, location_handler, start
# get environment variable from dotenv file
load_dotenv()

# load necessary env variable
TELEGRAM_API_TOKEN = os.getenv('TG_API_TOK')



# Hauptfunktion
def main():
    # Neue Initialisierung mit Application für Version 20+
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Befehle und Nachrichtenhandler registrieren
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, location_handler))
    # Bot starten
    application.run_polling()

if __name__ == '__main__':
    main()
