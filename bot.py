import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class FurnitureBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        if not self.token:
            raise ValueError("❌ TELEGRAM_TOKEN не найден! Добавьте его в переменные окружения.")
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
        logger.info("✅ Бот инициализирован")

    def setup_handlers(self):
        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("services", self.services_command))
        self.application.add_handler(CommandHandler("contacts", self.contacts_command))
        self.application.add_handler(CommandHandler("gallery", self.gallery_command))
        self.application.add_handler(CommandHandler("prices", self.prices_command))
        self.application.add_handler(CommandHandler("reviews", self.reviews_command))
        self.application.add_handler(CommandHandler("address", self.address_command))
        self.application.add_handler(CommandHandler("promotions", self.promotions_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Обработчик кнопок
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

        # Текстовые сообщения
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user

        keyboard = [
            [InlineKeyboardButton("🪑 Наши услуги", callback_data="services")],
            [InlineKeyboardButton("💰 Цены", callback_data="prices")],
            [InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
            [InlineKeyboardButton("📍 Адрес и маршрут", callback_data="address")],
            [InlineKeyboardButton("⭐ Отзывы", callback_data="reviews")],
            [InlineKeyboardButton("🎁 Акции", callback_data="promotions")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_text = f"""
🏠 Добро пожаловать в столярную мастерскую "Рассея", {user.first_name}!

Я ваш персональный помощник. Выберите нужный раздел:"""

        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        callback_data = query.data

        if callback_data == "services":
            await self.services_command(query, context)
        elif callback_data == "prices":
            await self.prices_command(query, context)
        elif callback_data == "contacts":
            await self.contacts_command(query, context)
        elif callback_data == "address":
            await self.address_command(query, context)
        elif callback_data == "reviews":
            await self.reviews_command(query, context)
        elif callback_data == "promotions":
            await self.promotions_command(query, context)

    async def services_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        services_text = """
🔧 НАШИ УСЛУГИ:

🪑 Изготовление мебели на заказ:
• Кухни любой сложности
• Шкафы-купе и гардеробные
• Столы и стулья
• Кровати и спальные гарнитуры
• Комоды и тумбы

🛠 Реставрация мебели:
• Восстановление антикварной мебели
• Замена фурнитуры
• Покраска и лакировка
• Ремонт любой сложности

🎯 Столярные работы:
• Межкомнатные двери
• Лестницы из дерева
• Окна и витражи
• Декоративные элементы
• Мебель по индивидуальным эскизам

💎 Работаем с породами дерева:
• Дуб, ясень, бук - премиум класс
• Сосна, ель - бюджетный вариант
• Красное дерево, орех - эксклюзив"""

        if hasattr(update, 'message'):
            await update.message.reply_text(services_text)
        else:
            await update.edit_message_text(services_text)

    async def contacts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        contacts_text = """
📞 КОНТАКТЫ МАСТЕРА:

👨‍🔧 Мастер: Константин
📱 Телефон: +7 (918) 307-76-22
📧 Email: ras@sea123.ru

💼 Профиль мастера:
• Опыт работы: 15 лет
• Специализация: мебель на заказ
• Выполнено проектов: 250+
• Гарантия на работы: 2 года

🕒 Режим работы:
Понедельник - Пятница: 9:00 - 18:00
Суббота: 10:00 - 16:00
Воскресенье: выходной

💬 Консультируем и делаем замеры БЕСПЛАТНО!"""

        if hasattr(update, 'message'):
            await update.message.reply_text(contacts_text)
        else:
            await update.edit_message_text(contacts_text)

    async def prices_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        prices_text = """
💰 ПРАЙС-ЛИСТ (ориентировочные цены):

🚪 МЕЖКОМНАТНЫЕ ДВЕРИ:
• Эконом (сосна) - от 5 000 руб.
• Стандарт (дуб) - от 8 000 руб.
• Премиум (красное дерево) - от 15 000 руб.

🪑 СТОЛЫ:
• Обеденные - от 10 000 руб.
• Письменные - от 8 000 руб.
• Журнальные - от 5 000 руб.
• Барные стойки - от 12 000 руб.

🛏 КРОВАТИ:
• Односпальные - от 15 000 руб.
• Двуспальные - от 20 000 руб.
• Детские - от 12 000 руб.
• С подъемным механизмом - от 25 000 руб.

🍳 КУХОННЫЕ ГАРНИТУРЫ:
• Прямые (до 2м) - от 35 000 руб.
• Угловые - от 50 000 руб.
• С островом - от 80 000 руб.
• С барной стойкой - от 60 000 руб.

📦 ШКАФЫ:
• Шкафы-купе - от 25 000 руб.
• Гардеробные - от 30 000 руб.
• Книжные - от 15 000 руб.
• Комоды - от 8 000 руб.

🎯 ДОПОЛНИТЕЛЬНО:
• Замеры - БЕСПЛАТНО
• Доставка - от 1 000 руб.
• Установка - от 2 000 руб.

💡 *Точная стоимость рассчитывается индивидуально!*
📞 *Звоните для бесплатной консультации: +7 (918) 307-76-22*"""

        if hasattr(update, 'message'):
            await update.message.reply_text(prices_text, parse_mode='Markdown')
        else:
            await update.edit_message_text(prices_text, parse_mode='Markdown')

    async def address_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        address_text = """
📍 НАШ АДРЕС:

🏭 Фабрика:
г. Апшеронск, ул. Фабричная, д. 28

🗺 Координаты для навигатора:
44.460656, 39.730243"""

        yandex_nav_url = "https://yandex.ru/maps/?mode=routes&rtext=~44.460656,39.730243&rtt=auto"

        keyboard = [
            [InlineKeyboardButton("🚗 Построить маршрут в Яндекс.Навигаторе", url=yandex_nav_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if hasattr(update, 'message'):
            await update.message.reply_text(address_text, reply_markup=reply_markup)
        else:
            await update.edit_message_text(address_text, reply_markup=reply_markup)

    async def promotions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        promotions_text = """
🎁 АКЦИИ И СПЕЦПРЕДЛОЖЕНИЯ:

🔥 ГОРЯЧЕЕ ПРЕДЛОЖЕНИЕ:
• Закажите кухню до конца месяца - получите скидку 15%!

🎉 ПОСТОЯННЫЕ АКЦИИ:
• При заказе от 50 000 руб. - доставка БЕСПЛАТНО
• Приведи друга - получи скидку 10% на следующий заказ
• Скидка пенсионерам - 5% на все работы

🆕 ДЛЯ НОВЫХ КЛИЕНТОВ:
• Первая консультация и замеры - БЕСПЛАТНО
• 3D-визуализация вашего проекта в подарок

📦 КОМПЛЕКСНЫЕ РЕШЕНИЯ:
• Кухня + обеденная группа = скидка 10%
• Спальня (кровать + 2 тумбы) = скидка 8%

💎 ЭКСКЛЮЗИВ:
• При заказе мебели из массива дуба - монтаж в ПОДАРОК!

📞 Успейте забронировать акцию: +7 (918) 307-76-22
⏰ Акции действуют до конца месяца!"""

        if hasattr(update, 'message'):
            await update.message.reply_text(promotions_text)
        else:
            await update.edit_message_text(promotions_text)

    async def reviews_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        reviews_text = """
⭐ ОТЗЫВЫ НАШИХ КЛИЕНТОВ:

1. 🏆 Анна - ⭐⭐⭐⭐⭐
   "Заказывала кухню из дуба. Качество превосходное! Мастер Константин очень внимательный, учёл все пожелания. Сделали быстрее оговоренного срока."

2. 🏆 Сергей - ⭐⭐⭐⭐⭐
   "Реставрировали старый комод. Выглядит как новый! Очень доволен работой, цены адекватные. Обязательно обращусь ещё."

3. 🏆 Мария - ⭐⭐⭐⭐⭐
   "Делали межкомнатные двери на дачу. Очень красиво и качественно! Все соседи спрашивают, кто делал. Спасибо за работу!"

4. 🏆 Дмитрий - ⭐⭐⭐⭐⭐
   "Заказывал шкаф-купе. Сделали точно в срок, качество на высоте! Цена ниже чем в магазинах."

5. 🏆 Ольга - ⭐⭐⭐⭐⭐
   "Изготовили детскую кровать. Ребенок в восторге! Материалы экологичные, обработка идеальная."

💫 Хотите так же? Звоните: +7 (918) 307-76-22"""

        if hasattr(update, 'message'):
            await update.message.reply_text(reviews_text)
        else:
            await update.edit_message_text(reviews_text)

    async def gallery_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        gallery_text = """
🖼 ГАЛЕРЕЯ НАШИХ РАБОТ:

📸 Наши работы:

🚪 Двери из массива дуба
• Классические модели
• Современный дизайн
• Резные элементы

🪑 Столы различного назначения
• Обеденные группы
• Письменные столы
• Барные стойки

🛏 Спальные гарнитуры
• Кровати двуспальные
• Детские кроватки
• Тумбы и комоды

🍳 Кухонные гарнитуры
• Прямые и угловые
• С барными стойками
• С островными элементами

📚 Шкафы и системы хранения
• Шкафы-купе
• Гардеробные системы
• Книжные полки

🎯 Каждый проект индивидуален!
📞 Присылайте ваши эскизы - реализуем любую идею!"""

        if hasattr(update, 'message'):
            await update.message.reply_text(gallery_text)
        else:
            await update.edit_message_text(gallery_text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
ℹ️ ПОМОЩЬ И КОМАНДЫ:

📋 Основные команды:
/start - Главное меню
/services - Наши услуги
/prices - Цены на изделия
/contacts - Контакты мастера
/address - Адрес и маршрут
/promotions - Акции и скидки
/reviews - Отзывы клиентов
/gallery - Галерея работ
/help - Эта справка

💡 Как сделать заказ:
1. Опишите что хотите - я помогу с выбором
2. Бесплатный выезд мастера на замеры
3. Согласование дизайна и материалов
4. Изготовление в оговоренные сроки
5. Доставка и установка

📞 Свяжитесь с нами:
Телефон: +7 (918) 307-76-22 (Константин)
Email: ras@sea123.ru
Адрес: г. Апшеронск, ул. Фабричная, д. 28

⏰ Режим работы: Пн-Пт 9:00-18:00, Сб 10:00-16:00"""

        if hasattr(update, 'message'):
            await update.message.reply_text(help_text)
        else:
            await update.edit_message_text(help_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text.lower()
        user = update.message.from_user

        logger.info(f"📨 Получено сообщение: '{user_message}' от {user.first_name}")

        if any(word in user_message for word in ['привет', 'здравств', 'добрый', 'hello', 'hi']):
            response = f"Привет, {user.first_name}! Рад вас видеть! Выберите раздел в меню или задайте вопрос."

        elif any(word in user_message for word in ['цена', 'стоимость', 'сколько стоит', 'ценник', 'прайс', 'price']):
            await self.prices_command(update, context)
            return

        elif any(word in user_message for word in ['мастер', 'константин', 'специалист', 'работник', 'master']):
            await self.contacts_command(update, context)
            return

        elif any(word in user_message for word in ['акция', 'акции', 'скидка', 'скидки', 'спец', 'промо', 'promo', 'discount']):
            await self.promotions_command(update, context)
            return

        elif any(word in user_message for word in ['адрес', 'адресе', 'location', 'location', 'где находитесь', 'как проехать', 'маршрут']):
            await self.address_command(update, context)
            return

        elif any(word in user_message for word in ['услуг', 'service', 'работы', 'делаете', 'изготовление']):
            await self.services_command(update, context)
            return

        elif any(word in user_message for word in ['отзыв', 'reviews', 'recommend', 'recommendation']):
            await self.reviews_command(update, context)
            return

        elif any(word in user_message for word in ['контакт', 'телефон', 'звонок', 'позвонить', 'связаться']):
            await self.contacts_command(update, context)
            return

        elif any(word in user_message for word in ['кухн', 'kitchen']):
            response = "🍳 Изготавливаем кухни на заказ от 35 000 рублей! Смотрите раздел /prices для ориентировочных цен и /services для подробностей."

        elif any(word in user_message for word in ['шкаф', 'гардероб', 'wardrobe']):
            response = "📦 Шкафы-купе и гардеробные от 25 000 рублей. Подробнее в разделе /prices"

        elif any(word in user_message for word in ['стол', 'table']):
            response = "🪑 Столы от 8 000 рублей. Можем сделать по вашему эскизу! Смотрите /prices"

        elif any(word in user_message for word in ['кровать', 'bed']):
            response = "🛏 Кровати от 12 000 рублей. Разные стили и материалы. /prices"

        elif any(word in user_message for word in ['двер', 'door']):
            response = "🚪 Двери межкомнатные от 5 000 рублей. Качество гарантируем! /prices"

        elif any(word in user_message for word in ['мебел', 'furniture']):
            response = "🪑 Изготавливаем мебель на заказ! Смотрите наши услуги в /services и цены в /prices"

        elif any(word in user_message for word in ['дерев', 'wood', 'массив', 'дуб', 'сосна']):
            response = "🌳 Работаем с дубом, ясенем, сосной и другими породами. Подробнее в /services"

        elif any(word in user_message for word in ['работы', 'портфолио', 'фото', 'галерея', 'пример']):
            await self.gallery_command(update, context)
            return

        else:
            response = "Не совсем понял ваш вопрос. Используйте кнопки меню или команды:\n\n" \
                      "/services - Услуги\n" \
                      "/prices - Цены\n" \
                      "/contacts - Контакты\n" \
                      "/address - Адрес\n" \
                      "/promotions - Акции\n" \
                      "/reviews - Отзывы\n" \
                      "/help - Помощь"

        await update.message.reply_text(response)

    def run(self):
        logger.info("🪚 Бот 'Рассея Мастерская' запускается...")
        logger.info("📞 Контакты: +7 (918) 307-76-22 Константин")
        logger.info("📍 Адрес: Апшеронск, ул. Фабричная, д. 28")
        
        # Используем polling для Railway
        logger.info("🚀 Запускаем бота в режиме polling...")
        self.application.run_polling()

if __name__ == '__main__':
    bot = FurnitureBot()
    bot.run()
