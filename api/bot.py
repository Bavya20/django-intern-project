import requests
from django.conf import settings
from .models import TelegramUser

BOT_TOKEN = settings.BOT_TOKEN
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"


def get_updates(offset=None):
    url = BASE_URL + "getUpdates"
    params = {"timeout": 10, "offset": offset}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["result"]
    return []


def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def check_telegram_messages():
    offset = None
    updates = get_updates(offset)

    for update in updates:
        if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            user_id = message["from"]["id"]
            username = message["from"].get("username", "")
            first_name = message["from"].get("first_name", "")

            text = message.get("text", "")
            if text == "/start":
                # Save to database if not already
                if not TelegramUser.objects.filter(telegram_id=user_id).exists():
                    TelegramUser.objects.create(
                        telegram_id=user_id,
                        username=username,
                        first_name=first_name,
                    )

                # Send welcome reply
                send_message(chat_id, f"Hello {first_name or username}! 🎉 You've been registered!")

        offset = update["update_id"] + 1
