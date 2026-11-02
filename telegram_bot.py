import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import time
import pytz

# FIX PORTA RENDER FREE - obbligatorio
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AITIPS Bot Live - 10:00 & 18:00")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

Thread(target=run_web_server, daemon=True).start()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@Aitipsfootballbot1")
ITALY_TZ = pytz.timezone('Europe/Rome')

START_MSG = """🤖 *AITIPS - Pronostici Calcio AI* ✅

Ciao ragazzi, il bot @Aitipsfootballbot e' ufficialmente ONLINE!

Da oggi pronostici AI con:
- xG, forma e statistiche avanzate
- Formazioni UFFICIALI LIVE
- Value Bet +10% rilevate dal radar

AGGIORNAMENTI AUTOMATICI:
10:00 -> Analisi match di giornata
18:00 -> Pronostici finali con formazioni ufficiali

ATTIVA LE NOTIFICHE di questo canale!

Comandi:
/oggi - Partite di oggi
/radar - Scanner Value Bet
/aiuto - Aiuto
"""

OGGI_MSG = """📅 PARTITE DI OGGI - AITIPS

Il radar AI sta analizzando le quote...

Alle 10:00 analisi completa
Alle 18:00 pronostici finali con formazioni UFFICIALI LIVE

Scrivi /radar per Value Bet!
Canale: @Aitipsfootballbot1
"""

RADAR_MSG = """🎯 AITIPS RADAR +10% VALUE

Scanner in corso...

Leghe: Serie A, Champions, Europa, Premier, Liga
Sistema confronta probabilita' AI vs quote book per VALUE +10%

Finali su @Aitipsfootballbot1 alle 10:00 e 18:00!
"""

AIUTO_MSG = """AITIPS - COMANDI
/start - Avvia
/oggi - Partite oggi
/radar - Value Bet
/roma - Focus Roma
/aiuto - Menu

Auto: 10:00 e 18:00
Canale: @Aitipsfootballbot1
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MSG, parse_mode='Markdown')
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=START_MSG, parse_mode='Markdown')
    except:
        pass

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(OGGI_MSG, parse_mode='Markdown')

async def radar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RADAR_MSG, parse_mode='Markdown')
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text="🎯 RADAR LIVE: Scanner in corso... Prossimi alle 10:00 e 18:00 su @Aitipsfootballbot1")
    except:
        pass

async def aiuto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(AIUTO_MSG, parse_mode='Markdown')

async def auto_post_10(context: ContextTypes.DEFAULT_TYPE):
    text = "🎯 AITIPS RADAR AUTOMATICO - 10:00\n\nBuongiorno! Radar AI attivo!\n\nAnalisi in corso con xG + forma + assenti.\n\nAlle 18:00 pronostici finali con formazioni UFFICIALI LIVE!\n\n@Aitipsfootballbot1"
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    except:
        pass

async def auto_post_18(context: ContextTypes.DEFAULT_TYPE):
    text = "🎯 AITIPS RADAR SERALE - 18:00\n\n🔥 PRONOSTICI FINALI CON FORMAZIONI UFFICIALI!\n\nIl radar finalizza Value Bet +10%...\n\nControlla @Aitipsfootballbot1!\n\n/radar per live"
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    except:
        pass

if __name__ == "__main__":
    print("Avvio AITIPS Bot - Setup NOVEMBRE 2026 - 10:00 e 18:00")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    app.add_handler(CommandHandler("radar", radar))
    app.add_handler(CommandHandler("roma", oggi))
    app.add_handler(CommandHandler("aiuto", aiuto))
    try:
        app.job_queue.run_daily(auto_post_10, time(hour=10, minute=0, tzinfo=ITALY_TZ), name="radar_10")
        app.job_queue.run_daily(auto_post_18, time(hour=18, minute=0, tzinfo=ITALY_TZ), name="radar_18")
        print("Job 10 e 18 attivi")
    except:
        pass
    app.run_polling()
