import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters  # Falls du Version 20 oder höher verwendest

# API-Schlüssel für OpenWeather
WEATHER_API_KEY = replaceme  # Ersetze dies mit deinem OpenWeather API-Schlüssel
TELEGRAM_API_TOKEN = replaceme  # Ersetze dies mit deinem Telegram Bot Token

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Funktion, um Wetterdaten von OpenWeather zu holen
def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=de"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
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

# Start-Befehl
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hallo! Sende mir deinen Standort, um das Wetter zu erfahren.")

# Funktion für Standort-Nachrichten
async def location_handler(update: Update, context: CallbackContext):
    if update.message.location:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        weather_info = get_weather(lat, lon)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Das ist kein gültiger Standort.")

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
