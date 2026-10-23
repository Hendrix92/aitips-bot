import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = "@Aitipsfootballbot1"

async def radar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"AITIPS RADAR +10% VALUE\n\nBot: @Aitipsfootballbot LIVE 24/7\nCanale: https://t.me/Aitipsfootballbot1\n\n17 leghe - Solo pick con +10% valore reale\nSerie A, Premier, UCL: troppo efficienti oggi"
    await update.message.reply_text(msg)
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=msg)
    except:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono AITIPS @Aitipsfootballbot - Usa /radar")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("radar", radar))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("champions", radar))
print("AITIPS Bot @Aitipsfootballbot partito")
app.run_polling()
