from django.core.management.base import BaseCommand
from api.bot import check_telegram_messages

class Command(BaseCommand):
    help = 'Check Telegram for /start messages'

    def handle(self, *args, **kwargs):
        check_telegram_messages()
        self.stdout.write("✔ Telegram checked.")
