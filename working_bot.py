import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

# Включаем подробное логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

TOKEN = os.getenv('TELEGRAM_TOKEN')
print(f"🔑 Токен загружен: {TOKEN}")

# Главное меню
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🪑 НАШИ УСЛУГИ", callback_data="services")],
        [InlineKeyboardButton("💰 ЦЕНЫ", callback_data="prices")],
        [InlineKeyboardButton("📞 КОНТАКТЫ", callback_data="contacts")],
        [InlineKeyboardButton("📍 АДРЕС", callback_data="address")],
        [InlineKeyboardButton("⭐ ОТЗЫВЫ", callback_data="reviews")],
        [InlineKeyboardButton("🎁 АКЦИИ", callback_data="promotions")],
        [InlineKeyboardButton("👨‍💻 АВТОР", callback_data="developer")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Кнопка назад
def back_button():
    keyboard = [[InlineKeyboardButton("🔙 НАЗАД", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔄 Команда /start получена")
    
    user = update.message.from_user
    welcome_text = f"""🏠 Добро пожаловать в мастерскую "РАССЕЯ"!

{user.first_name}, выберите раздел:"""
    
    await update.message.reply_text(welcome_text, reply_markup=main_menu())
    print("✅ Меню отправлено")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔄 Обработчик кнопок ВЫЗВАН")
    
    query = update.callback_query
    await query.answer()
    
    data = query.data
    print(f"📨 Нажата кнопка: {data}")
    
    if data == "services":
        text = """🔧 НАШИ УСЛУГИ:

• 🍳 Кухни на заказ
• 🚪 Шкафы-купе  
• 🛏 Кровати
• 🪑 Столы и стулья
• 🛠 Реставрация мебели
• 🎯 Межкомнатные двери

📞 +7 (918) 307-76-22"""
        print("✅ Услуги отправлены")
        
    elif data == "prices":
        text = """💰 ЦЕНЫ:

• Двери: от 5 000 руб.
• Столы: от 8 000 руб. 
• Кровати: от 12 000 руб.
• Кухни: от 35 000 руб.

📞 +7 (918) 307-76-22"""
        print("✅ Цены отправлены")
        
    elif data == "contacts":
        text = """📞 КОНТАКТЫ:

👨‍🔧 Мастер: Константин
📱 Телефон: +7 (918) 307-76-22
📧 Email: ras@sea123.ru

🕒 Пн-Пт: 9:00-18:00"""
        print("✅ Контакты отправлены")
        
    elif data == "address":
        text = """📍 АДРЕС:

г. Апшеронск
ул. Фабричная, д. 28

Координаты:
44.460656, 39.730243"""
        
        # Кнопка Яндекс карт
        yandex_url = "https://yandex.ru/maps/?mode=routes&rtext=~44.460656,39.730243"
        keyboard = [
            [InlineKeyboardButton("🗺️ ЯНДЕКС КАРТЫ", url=yandex_url)],
            [InlineKeyboardButton("🔙 НАЗАД", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        print("✅ Адрес отправлен")
        return
        
    elif data == "reviews":
        text = """⭐ ОТЗЫВЫ:

1. Анна: "Кухня супер!"
2. Сергей: "Качество отличное!"
3. Мария: "Рекомендую!"

📞 +7 (918) 307-76-22"""
        print("✅ Отзывы отправлены")
        
    elif data == "promotions":
        text = """🎁 АКЦИИ:

• Скидка 15% на кухни
• Бесплатная доставка
• Скидка пенсионерам

📞 +7 (918) 307-76-22"""
        print("✅ Акции отправлены")
        
    elif data == "developer":
        text = """👨‍💻 АВТОР БОТА:

Роман Львович
📱 +7 (981) 931-24-82
📧 trainingsw75@gmail.com

Создание Telegram ботов"""
        print("✅ Инфо об авторе отправлена")
        
    elif data == "back":
        await query.edit_message_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )
        print("✅ Возврат в меню")
        return
    
    # Для всех остальных кнопок добавляем кнопку "Назад"
    await query.edit_message_text(text, reply_markup=back_button())
    print(f"✅ Текст для {data} отправлен")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"📨 Получено сообщение: {update.message.text}")
    await update.message.reply_text(
        "Используйте /start для меню",
        reply_markup=main_menu()
    )

def main():
    print("=" * 50)
    print("🪚 ЗАПУСКАЕМ БОТА 'РАССЕЯ'")
    print("📞 Мастер: +7 (918) 307-76-22")
    print("👨‍💻 Разработчик: +7 (981) 931-24-82")
    print("=" * 50)
    
    try:
        app = Application.builder().token(TOKEN).build()
        print("✅ Приложение создано")
        
        app.add_handler(CommandHandler("start", start))
        print("✅ Обработчик /start добавлен")
        
        app.add_handler(CallbackQueryHandler(button_handler))
        print("✅ Обработчик кнопок добавлен")
        
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("✅ Обработчик сообщений добавлен")
        
        print("🚀 Бот запускается...")
        print("👉 Напишите боту: /start")
        print("🎯 Нажимайте ВСЕ кнопки!")
        
        app.run_polling()
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
