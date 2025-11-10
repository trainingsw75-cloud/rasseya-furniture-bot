import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ВКЛЮЧАЕМ ЛОГИРОВАНИЕ ДЛЯ ДЕБАГА
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Меняем на DEBUG чтобы видеть ВСЁ
)

TOKEN = os.getenv('TELEGRAM_TOKEN')
print("🔄 Загружаем токен...")

# Главное меню
def get_main_menu():
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
    print("✅ /start команда получена!")
    await update.message.reply_text(
        "🏠 Выберите раздел:",
        reply_markup=get_main_menu()
    )

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🎯 КНОПКА НАЖАТА! Обработчик вызван!")
    
    query = update.callback_query
    await query.answer()  # Важно: подтверждаем нажатие
    
    print(f"📊 Данные кнопки: {query.data}")
    
    # Обрабатываем разные кнопки
    if query.data == "services":
        response = "🔧 УСЛУГИ:\n• Кухни на заказ\n• Шкафы-купе\n• Межкомнатные двери\n• Реставрация мебели"
    elif query.data == "prices":
        response = "💰 ЦЕНЫ:\n• Двери: от 5 000 руб.\n• Столы: от 8 000 руб.\n• Кухни: от 35 000 руб."
    elif query.data == "contacts":
        response = "📞 КОНТАКТЫ:\nМастер: Константин\nТелефон: +7 (918) 307-76-22"
    elif query.data == "address":
        response = "📍 АДРЕС:\nг. Апшеронск\nул. Фабричная, д. 28"
    elif query.data == "reviews":
        response = "⭐ ОТЗЫВЫ:\nКлиенты довольны качеством!\nРейтинг: 5⭐"
    elif query.data == "promotions":
        response = "🎁 АКЦИИ:\n• Скидка 15% на кухни\n• Бесплатная доставка"
    elif query.data == "developer":
        response = "👨‍💻 АВТОР БОТА:\nРоман Львович\n+7 (981) 931-24-82"
    else:
        response = "Неизвестная команда"
    
    print(f"📤 Отправляем ответ: {response}")
    
    # ОБНОВЛЯЕМ сообщение с новым текстом
    await query.edit_message_text(
        text=response,
        reply_markup=get_main_menu()  # Возвращаем меню
    )

def main():
    print("🚀 ЗАПУСКАЕМ БОТА С РАБОЧИМИ КНОПКАМИ...")
    
    try:
        # Создаём приложение
        application = Application.builder().token(TOKEN).build()
        print("✅ Приложение создано")
        
        # ДОБАВЛЯЕМ ОБРАБОТЧИКИ
        application.add_handler(CommandHandler("start", start_command))
        print("✅ Обработчик /start добавлен")
        
        application.add_handler(CallbackQueryHandler(handle_button_click))
        print("✅ Обработчик кнопок добавлен")
        
        # Запускаем бота
        print("🎯 Бот запущен! Тестируйте:")
        print("1. Напишите /start")
        print("2. НАЖМИТЕ на любую кнопку")
        print("3. Должен появиться текст!")
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
