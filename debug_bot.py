import os
from dotenv import load_dotenv

# ЯВНО указываем путь к .env файлу
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"🔍 Ищем .env файл по пути: {dotenv_path}")

load_dotenv(dotenv_path)

# Проверяем токен
TOKEN = os.getenv('TELEGRAM_TOKEN')
print(f"🔑 Токен из .env: {TOKEN}")

if not TOKEN:
    print("❌ ТОКЕН НЕ НАЙДЕН! Проверь:")
    print("1. Файл .env существует?")
    print("2. Содержит TELEGRAM_TOKEN=твой_токен?")
    print("3. Файл в той же папке что и бот?")
    exit(1)

print("✅ Токен загружен успешно!")

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🪑 УСЛУГИ", callback_data="services")],
        [InlineKeyboardButton("💰 ЦЕНЫ", callback_data="prices")],
        [InlineKeyboardButton("📞 КОНТАКТЫ", callback_data="contacts")],
        [InlineKeyboardButton("📍 АДРЕС", callback_data="address")],
        [InlineKeyboardButton("⭐ ОТЗЫВЫ", callback_data="reviews")],
        [InlineKeyboardButton("🎁 АКЦИИ", callback_data="promotions")],
        [InlineKeyboardButton("👨‍💻 АВТОР", callback_data="developer")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start получен!")
    await update.message.reply_text(
        "🏠 Выберите раздел:",
        reply_markup=main_menu()
    )

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🎯 КНОПКА НАЖАТА!")
    
    query = update.callback_query
    await query.answer()
    
    if query.data == "services":
        response = "🔧 УСЛУГИ:\n• Кухни\n• Шкафы\n• Двери\n• Реставрация"
    elif query.data == "prices":
        response = "💰 ЦЕНЫ:\n• Двери: от 5 000 руб.\n• Столы: от 8 000 руб."
    elif query.data == "contacts":
        response = "📞 КОНТАКТЫ:\n+7 (918) 307-76-22\nКонстантин"
    elif query.data == "address":
        response = "📍 АДРЕС:\nг. Апшеронск\nул. Фабричная, д. 28"
    elif query.data == "reviews":
        response = "⭐ ОТЗЫВЫ:\nКлиенты довольны!"
    elif query.data == "promotions":
        response = "🎁 АКЦИИ:\n• Скидка 15%\n• Бесплатная доставка"
    elif query.data == "developer":
        response = "👨‍💻 АВТОР:\nРоман Львович\n+7 (981) 931-24-82"
    else:
        response = "Неизвестная команда"
    
    await query.edit_message_text(response, reply_markup=main_menu())

def main():
    print("🚀 ЗАПУСК БОТА...")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_button_click))
    
    print("✅ Бот запущен! Тестируй /start")
    app.run_polling()

if __name__ == '__main__':
    main()
