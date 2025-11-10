import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"🎯 /start от: {user.first_name}")
    
    keyboard = [
        [InlineKeyboardButton("🪑 УСЛУГИ", callback_data="services")],
        [InlineKeyboardButton("💰 ЦЕНЫ", callback_data="prices")],
        [InlineKeyboardButton("📞 КОНТАКТЫ", callback_data="contacts")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Привет {user.first_name}! Выберите раздел:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔥 КНОПКА НАЖАТА!")
    
    query = update.callback_query
    await query.answer()
    
    print(f"📊 Нажата: {query.data}")
    
    if query.data == "services":
        text = "🔧 УСЛУГИ:\n• Кухни\n• Шкафы\n• Двери\n📞 +7 (918) 307-76-22"
    elif query.data == "prices":
        text = "💰 ЦЕНЫ:\n• От 5 000 руб.\n📞 +7 (918) 307-76-22"
    elif query.data == "contacts":
        text = "📞 КОНТАКТЫ:\n+7 (918) 307-76-22\nКонстантин"
    else:
        text = "Неизвестная команда"
    
    await query.edit_message_text(text)
    print("✅ Сообщение обновлено!")

def main():
    print("🚀 Бот запускается на Railway...")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот запущен! Ожидаем сообщения...")
    app.run_polling()

if __name__ == '__main__':
    main()
