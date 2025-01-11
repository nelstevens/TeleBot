import os
import requests
import logging
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

# get necessary env variables
WEATHER_API_KEY = os.getenv('WT_API_KEY')

# set location
LOC = range(1)
# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)



# Start-Befehl
async def weather_start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hallo! Sende mir deinen Standort, um das Wetter zu erfahren.")

    return LOC

# Funktion, um Wetterdaten von OpenWeather zu holen
def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=de"
    logger.info(url)
    response = requests.get(url)
    logger.info(response)
    if response.status_code == 200:
        data = response.json()
        logger.info(data)
        weather = data['weather'][0]['description']  # Allgemeine Wetterbeschreibung (z.B. "klar", "bewölkt")
        temp = data['main']['temp']  # Aktuelle Temperatur
        city = data['name']  # Stadtname
        humidity = data['main']['humidity']  # Luftfeuchtigkeit
        wind_speed = data['wind']['speed']  # Windgeschwindigkeit
        pressure = data['main']['pressure']  # Luftdruck
        
        # Formatierte Ausgabe der Wetterdaten
        weather_info = (
            f"Das Wetter in {city}:\n"
            f"{weather.capitalize()}\n"
            f"Temperatur: {temp}°C\n"
            f"Luftfeuchtigkeit: {humidity}%\n"
            f"Windgeschwindigkeit: {wind_speed} m/s\n"
            f"Luftdruck: {pressure} hPa"
        )
        return weather_info
    else:
        return "Entschuldigung, ich konnte die Wetterdaten nicht abrufen. Bitte versuche es später erneut."


# Funktion für Standort-Nachrichten
async def location_handler(update: Update, context: CallbackContext):
    if update.message.location:
        lat = update.message.location.latitude
        logger.info(lat)
        lon = update.message.location.longitude
        logger.info(lon)
        weather_info = get_weather(lat, lon)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Das ist kein gültiger Standort.")
    
    return ConversationHandler.END

# set cancel handler
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Bye!")

    return ConversationHandler.END

# create conversation Handler
weather_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("weather", weather_start)],
    states={
        LOC: [MessageHandler(filters.LOCATION, location_handler)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)