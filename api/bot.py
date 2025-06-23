import requests
from django.conf import settings
from .models import TelegramUser

URL = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/getUpdates"

def check_telegram_messages():
    response = requests.get(URL)
    data = response.json()

    for update in data.get('result', []):
        message = update.get('message')
        if message and message.get('text') == '/start':
            username = message['from'].get('username')
            if username:
                TelegramUser.objects.get_or_create(username=username)
