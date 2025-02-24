import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

import jdatetime # convert miladi to jalali calender
from datetime import datetime

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(r'سلام عزیز. برای مشاهده تقویم \time رو برام بنویس')

# get miladi and jalali time
async def time (update: Update, context: CallbackContext) -> None:
    now = datetime.now()
    # convert datetime to jalaliDatetime
    jalali_date = jdatetime.datetime.fromgregorian(datetime=now)
    await update.message.reply_text(f"تاری میلادی: {now} \n تاریخ شمسی: {str(jalali_date)} ")


async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

async def error(update: Update, context: CallbackContext) -> None:
    print(f'Error: {context.error}')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).connect_timeout(30).read_timeout(30).build()

    # /start
    application.add_handler(CommandHandler("start", start))

    # echo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # /time
    application.add_handler(CommandHandler("time" , time))

    application.add_error_handler(error)

    application.run_polling()

if __name__ == '__main__':
    main()
