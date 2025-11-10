import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "7145387936:AAFq9lHwljHttizWCvF6ajS4DzwNHt510MU"
print(f"🔑 Токен: {TOKEN}")

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🪑 УСЛУГИ", callback_data="services")],
        [InlineKeyboardButton("💰 ЦЕНЫ", callback_data="prices")],
        [InlineKeyboardButton("📞 КОНТАКТЫ", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"✅ /start от: {update.message.from_user.first_name}")
    await update.message.reply_text(
        "🏠 ВЫБЕРИТЕ РАЗДЕЛ (нажмите кнопку):",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🎯 КНОПКА НАЖАТА! ОБРАБОТЧИК ВЫЗВАН!")
    
    query = update.callback_query
    await query.answer()
    
    print(f"📊 Нажата кнопка: {query.data}")
    
    if query.data == "services":
        response = "🔧 НАШИ УСЛУГИ:\n• Кухни на заказ\n• Шкафы-купе\n• Межкомнатные двери\n• Реставрация мебели\n\n📞 +7 (918) 307-76-22"
    elif query.data == "prices":
        response = "💰 ЦЕНЫ:\n• Двери: от 5 000 руб.\n• Столы: от 8 000 руб.\n• Кухни: от 35 000 руб.\n\n📞 +7 (918) 307-76-22"
    elif query.data == "contacts":
        response = "📞 КОНТАКТЫ:\n👨‍🔧 Мастер: Константин\n📱 +7 (918) 307-76-22\n📧 ras@sea123.ru\n📍 Апшеронск, ул. Фабричная, 28"
    else:
        response = "❌ Неизвестная команда"
    
    await query.edit_message_text(
        text=response,
        reply_markup=main_menu()
    )
    print("✅ Сообщение обновлено!")

def main():
    print("=" * 50)
    print("🚀 ЗАПУСКАЕМ БОТА С РАБОЧИМИ КНОПКАМИ")
    print("=" * 50)
    
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Обработчики добавлены!")
    print("🎯 ИНСТРУКЦИЯ:")
    print("   1. Напишите боту: /start")
    print("   2. НАЖМИТЕ на любую кнопку")
    print("   3. Должен появиться текст!")
    print("=" * 50)
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
