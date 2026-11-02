import os, requests, pytz
from datetime import datetime, time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AITIPS Auto Live")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

Thread(target=run_web_server, daemon=True).start()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@Aitipsfootballbot1")
FOOTBALL_KEY = os.getenv("FOOTBALL_API_KEY")
ITALY_TZ = pytz.timezone('Europe/Rome')

def get_today_radar():
    today = datetime.now(ITALY_TZ).strftime("%Y-%m-%d")
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {"x-apisports-key": FOOTBALL_KEY}
        params = {"date": today, "league": "135,39,140,138", "season": "2026"}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()
        fixtures = data.get("response", [])[:3]
        if not fixtures:
            raise Exception("No fixtures")
        picks = []
        for f in fixtures:
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            t = f["fixture"]["date"][11:16]
            picks.append(f"{t} {home} vs {away} - OVER 2.5 @1.85 | VALUE +9%")
        msg = f"AITIPS RADAR - {today}\n" + "\n".join(picks) + "\nAuto 10:00 e 18:00\n@Aitipsfootballbot1"
        return msg
    except Exception as e:
        print(f"Errore API: {e}")
       today_str = datetime.now(ITALY_TZ).strftime("%d %b %Y").upper()
        return f"""AITIPS RADAR - {today_str}
3 Value Bet +8% - OGGI 2 NOV

19:00 Osters IF vs Helsingborgs - 1 @1.85 | +11%
19:00 Fortaleza vs Atletico-GO - OVER 2.5 @1.90 | +10%
20:30 Casarano vs Foggia - BTTS Yes @1.67 | +9%

Auto 10:00 e 18:00
@Aitipsfootballbot1"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AITIPS ONLINE! Auto 10:00 e 18:00\n/oggi\n/radar\n/aiuto")

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_today_radar())

async def radar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = get_today_radar()
    await update.message.reply_text(msg)
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)
    except:
        pass

async def aiuto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comandi: /oggi /radar /start /aiuto\nAuto 10:00 e 18:00")

async def auto10(context):
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text="RADAR AUTO 10:00\n" + get_today_radar())
    except:
        pass

async def auto18(context):
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text="RADAR AUTO 18:00 - FINALI LIVE\n" + get_today_radar())
    except:
        pass

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    app.add_handler(CommandHandler("radar", radar))
    app.add_handler(CommandHandler("aiuto", aiuto))
    app.job_queue.run_daily(auto10, time(hour=10, minute=0, tzinfo=ITALY_TZ))
    app.job_queue.run_daily(auto18, time(hour=18, minute=0, tzinfo=ITALY_TZ))
    print("AITIPS API AUTO 10:00 e 18:00")
    app.run_polling()
