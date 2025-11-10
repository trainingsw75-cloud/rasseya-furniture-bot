import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_TOKEN')

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🪑 НАШИ УСЛУГИ", callback_data="services")],
        [InlineKeyboardButton("💰 ЦЕНЫ И РАСЧЁТ", callback_data="prices")],
        [InlineKeyboardButton("📞 КОНТАКТЫ МАСТЕРА", callback_data="contacts")],
        [InlineKeyboardButton("📍 АДРЕС И КАРТА", callback_data="address")],
        [InlineKeyboardButton("⭐ ОТЗЫВЫ КЛИЕНТОВ", callback_data="reviews")],
        [InlineKeyboardButton("🎁 АКЦИИ И СКИДКИ", callback_data="promotions")],
        [InlineKeyboardButton("👨‍💻 АВТОР БОТА", callback_data="developer")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    welcome_text = f"""🏠 Добро пожаловать в столярную мастерскую "РАССЕЯ"!

{user.first_name}, я ваш персональный помощник!

🎯 Выберите нужный раздел:"""
    
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    logger.info(f"Нажата кнопка: {callback_data}")
    
    if callback_data == "services":
        text = """🔧 НАШИ УСЛУГИ:

🪑 Изготовление мебели на заказ:
• Кухни любой сложности
• Шкафы-купе и гардеробные
• Столы и стулья
• Кровати и спальные гарнитуры

🛠 Реставрация мебели:
• Восстановление антикварной мебели
• Замена фурнитуры
• Покраска и лакировка

🎯 Столярные работы:
• Межкомнатные двери
• Лестницы из дерева
• Окна и витражи

📞 Телефон: +7 (918) 307-76-22"""
        
    elif callback_data == "prices":
        text = """💰 ПРАЙС-ЛИСТ:

🚪 Двери: от 5 000 руб.
🪑 Столы: от 8 000 руб.
🛏 Кровати: от 12 000 руб.
🍳 Кухни: от 35 000 руб.

📞 Звоните для расчёта: +7 (918) 307-76-22"""
        
    elif callback_data == "contacts":
        text = """📞 КОНТАКТЫ:

👨‍🔧 Мастер: Константин
📱 Телефон: +7 (918) 307-76-22
📧 Email: ras@sea123.ru

🕒 Режим работы:
Пн-Пт: 9:00-18:00
Сб: 10:00-16:00"""
        
    elif callback_data == "address":
        text = """📍 АДРЕС:

г. Апшеронск, ул. Фабричная, д. 28

Координаты: 44.460656, 39.730243"""
        
        yandex_url = "https://yandex.ru/maps/?mode=routes&rtext=~44.460656,39.730243"
        keyboard = [
            [InlineKeyboardButton("🗺️ ОТКРЫТЬ В ЯНДЕКС.КАРТАХ", url=yandex_url)],
            [InlineKeyboardButton("🔙 НАЗАД В МЕНЮ", callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)
        return
        
    elif callback_data == "reviews":
        text = """⭐ ОТЗЫВЫ КЛИЕНТОВ:

1. 🏆 Анна - ⭐⭐⭐⭐⭐
"Заказывала кухню из дуба. Качество превосходное!"

2. 🏆 Сергей - ⭐⭐⭐⭐⭐  
"Реставрировали старый комод. Выглядит как новый!"

3. 🏆 Мария - ⭐⭐⭐⭐⭐
"Делали межкомнатные двери. Очень красиво и качественно!"

📞 +7 (918) 307-76-22"""
        
    elif callback_data == "promotions":
        text = """🎁 АКЦИИ И СКИДКИ:

🔥 Скидка 15% на кухни
🎉 Бесплатная доставка от 50 000 руб.
👵 Скидка пенсионерам 5%

📞 +7 (918) 307-76-22"""
        
    elif callback_data == "developer":
        text = """👨‍💻 АВТОР БОТА:

Роман Львович
📱 Телефон: +7 (981) 931-24-82
📧 Email: trainingsw75@gmail.com

💼 Создание Telegram ботов
🎯 Python разработка"""
        
    elif callback_data == "back_menu":
        await query.edit_message_text(
            "🏠 Главное меню:\nВыберите раздел:",
            reply_markup=main_menu_keyboard()
        )
        return
    
    # Кнопка назад для всех разделов
    keyboard = [[InlineKeyboardButton("🔙 НАЗАД В МЕНЮ", callback_data="back_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Используйте /start для открытия меню",
        reply_markup=main_menu_keyboard()
    )

def main():
    print("🪚 Запускаем бота 'РАССЕЯ'...")
    print("📞 Контакты: +7 (918) 307-76-22")
    print("👨‍💻 Разработчик: +7 (981) 931-24-82")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен! Тестируйте /start")
    app.run_polling()

if __name__ == '__main__':
    main()
