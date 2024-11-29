import os
import re
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters

# توکن ربات
TOKEN = os.getenv("BOT_TOKEN")  # توکن ربات از متغیر محیطی

# شناسه کانال مقصد
DESTINATION_CHANNEL = os.getenv("DESTINATION_CHANNEL")  # نام کانال مقصد از متغیر محیطی

# تگ‌های قدیمی و جدید
OLD_TAG = "@iMTProto"
NEW_TAG = "@MProxyProtoT"

def forward_message(update, context):
    # دریافت متن پیام
    message_text = update.message.text

    # پیدا کردن لینک‌ها در متن پیام
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_text)

    # حذف تگ قدیمی و جایگزینی با تگ جدید
    modified_text = re.sub(OLD_TAG, NEW_TAG, message_text)

    # ساخت پیام جدید که شامل لینک‌ها نیز باشد
    if urls:
        # اضافه کردن لینک‌ها به انتهای متن
        modified_text += "\n\nلینک‌ها:\n" + "\n".join(urls)

    # ارسال پیام به کانال مقصد
    context.bot.send_message(chat_id=DESTINATION_CHANNEL, text=modified_text)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # از هر پیامی که در کانال‌ها دریافت می‌شود استفاده می‌کنیم
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
