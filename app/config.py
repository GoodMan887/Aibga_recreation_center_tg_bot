import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    exit("Ошибка: BOT_TOKEN не найден в переменной окружения!")

# BUTTON_DIRECTIONS = "🎨 Направления и условия"
# BUTTON_BOOKING = "✨ Записаться на пробное"
# BUTTON_PARTNERSHIP = "🤝 Предложить услуги"
