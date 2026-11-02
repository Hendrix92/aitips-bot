import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AITIPS Live")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

Thread(target=run_web_server, daemon=True).start()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@Aitipsfootballbot1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 AITIPS ONLINE!\n\n10:00 Analisi giornata\n18:00 Pronostici finali con formazioni LIVE\n\n/oggi - Partite oggi\n/radar - Value Bet\n/aiuto - Info\nCanale @Aitipsfootballbot1")

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 PARTITE OGGI - AITIPS\n\n10:00 analisi\n18:00 finali con formazioni UFFICIALI LIVE\n\n/radar per Value Bet!")

async def radar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 AITIPS RADAR +10% VALUE\n\nScanner in corso... Serie A, Champions, Europa, Premier, Liga\n\nFinali su @Aitipsfootballbot1 alle 10:00 e 18:00!")

async def aiuto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🆘 AITIPS\n/start - Avvia\n/oggi - Oggi\n/radar - Value Bet\n/aiuto - Info\n\nAuto 10:00 e 18:00")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("oggi", oggi))
app.add_handler(CommandHandler("radar", radar))
app.add_handler(CommandHandler("aiuto", aiuto))
app.run_polling()
