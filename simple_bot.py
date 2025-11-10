import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен прямо в коде (временно для теста)
TOKEN = "7145387936:AAFq9lHwljHttizWCvF6ajS4DzwNHt510MU"

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🪑 УСЛУГИ", callback_data="services")],
        [InlineKeyboardButton("💰 ЦЕНЫ", callback_data="prices")],
        [InlineKeyboardButton("📞 КОНТАКТЫ", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери:", reply_markup=main_menu())

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "services":
        await query.edit_message_text("🔧 УСЛУГИ!")
    elif query.data == "prices":
        await query.edit_message_text("💰 ЦЕНЫ!")
    elif query.data == "contacts":
        await query.edit_message_text("📞 КОНТАКТЫ!")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))

print("🚀 Бот запущен!")
app.run_polling()
