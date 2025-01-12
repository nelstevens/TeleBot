import requests
from datetime import datetime
import logging
from telegram import Update, constants
from telegram.ext import CallbackContext

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)



def get_busdepartures(station_name: str):
    url = f"https://transport.opendata.ch/v1/stationboard?station={station_name}&limit=10&transportations=bus"
    logger.info(url)
    response = requests.get(url).json()
    logger.info(response)
    sb = response["stationboard"]
    flt = [x for x in sb if x['number'] == '66' and x['to'] in ('Enge', 'Zürich, Morgental')]
    strs = []
    for x in sb:
        if x['number'] == '66' and x['to'] in ('Enge', 'Zürich, Morgental'):
            dep = datetime.fromtimestamp(x['stop']['departureTimestamp']).strftime("%H:%M")
            dest = x['to']
            bs_nr = x.get('number', 'unbekannt')
            delay = x['stop'].get('delay', 0)
            strng = f"Bus: {bs_nr} in Richtung {dest}\nAbfahrt: {dep}\nVerspätung: {delay}\n\n"
            strs.append(strng)
    
    return f'*Abfahrten {station_name}:*\n\n' + ''.join(strs)

async def bus_start(update: Update, context: CallbackContext):
    breitloo = get_busdepartures("Breitloo")
    await update.message.reply_text(breitloo, parse_mode=constants.ParseMode.MARKDOWN_V2)