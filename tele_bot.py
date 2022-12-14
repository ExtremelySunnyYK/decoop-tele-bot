import os
import time
import datetime as DT
from telegram import Bot
from telegram import ParseMode
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv("keys.env")
token = str(os.getenv("TELEGRAM_BOT"))
chatid = int(os.getenv("CHAT_ID"))
bot = Bot(token=token)

def scanner():
    try:
        # bot = Bot(token=token)
        bot.sendMessage(
            text="🎁 ",
            timeout=200, disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
            )

    except Exception as e:
        print(e)

    return True


def on_error(self, status):
    time.sleep(200)
    print(status.text)


def on_error(self, status_code):
    if status_code == 420:
        time.sleep(60)
        return False


