import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# МАКСИМАЛЬНОЕ ЛОГИРОВАНИЕ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# Токен прямо в коде для уверенности
TOKEN = "7145387936:AAFq9lHwljHttizWCvF6ajS4DzwNHt510MU"
print(f"🔑 Токен: {TOKEN}")

def main_menu():
    print("🔄 Создаём меню...")
    keyboard = [
        [InlineKeyboardButton("🪑 УСЛУГИ", callback_data="services")],
        [InlineKeyboardButton("💰 ЦЕНЫ", callback_data="prices")],
        [InlineKeyboardButton("📞 КОНТАКТЫ", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"✅ /start от пользователя: {update.message.from_user.first_name}")
    await update.message.reply_text(
        "🏠 ВЫБЕРИТЕ РАЗДЕЛ (нажмите кнопку):",
        reply_markup=main_menu()
    )
    print("✅ Меню отправлено!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🎯🎯🎯 КНОПКА НАЖАТА! ОБРАБОТЧИК ВЫЗВАН! 🎯🎯🎯")
    
    query = update.callback_query
    print(f"📊 Callback data: {query.data}")
    print(f"📊 Message: {query.message}")
    
    # ОБЯЗАТЕЛЬНО подтверждаем нажатие
    await query.answer()
    print("✅ Query.answer() выполнен")
    
    # Обрабатываем кнопки
    if query.data == "services":
        response = "🔧 НАШИ УСЛУГИ:\n• Кухни на заказ\n• Шкафы-купе\n• Межкомнатные двери\n• Реставрация мебели\n\n📞 +7 (918) 307-76-22"
    elif query.data == "prices":
        response = "💰 ЦЕНЫ:\n• Двери: от 5 000 руб.\n• Столы: от 8 000 руб.\n• Кухни: от 35 000 руб.\n• Бесплатный замер!\n\n📞 +7 (918) 307-76-22"
    elif query.data == "contacts":
        response = "📞 КОНТАКТЫ:\n👨‍🔧 Мастер: Константин\n📱 Телефон: +7 (918) 307-76-22\n📧 Email: ras@sea123.ru\n📍 Адрес: Апшеронск, ул. Фабричная, 28"
    else:
        response = "❌ Неизвестная команда"
    
    print(f"📤 ОТПРАВЛЯЕМ ОТВЕТ: {response}")
    
    # ОБНОВЛЯЕМ сообщение
    await query.edit_message_text(
        text=response,
        reply_markup=main_menu()  # Возвращаем меню
    )
    print("✅ Сообщение обновлено!")

def main():
    print("=" * 50)
    print("🚀 ЗАПУСКАЕМ СУПЕР-БОТА С РАБОЧИМИ КНОПКАМИ")
    print("=" * 50)
    
    try:
        # Создаём приложение
        print("1. Создаём Application...")
        application = Application.builder().token(TOKEN).build()
        print("✅ Application создан")
        
        # ДОБАВЛЯЕМ ОБРАБОТЧИКИ
        print("2. Добавляем обработчик /start...")
        application.add_handler(CommandHandler("start", start_command))
        print("✅ Обработчик /start добавлен")
        
        print("3. Добавляем обработчик кнопок...")
        application.add_handler(CallbackQueryHandler(button_handler))
        print("✅ Обработчик кнопок добавлен")
        
        print("4. Проверяем handlers...")
        print(f"   Всего handlers: {len(application.handlers)}")
        for i, handler in enumerate(application.handgers):
            print(f"   Handler {i}: {handler}")
        
        # Запускаем
        print("5. Запускаем бота...")
        print("🎯 ИНСТРУКЦИЯ:")
        print("   • Напишите боту: /start")
        print("   • НАЖМИТЕ на кнопку 'УСЛУГИ'")
        print("   • Должен появиться текст про услуги!")
        print("=" * 50)
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
