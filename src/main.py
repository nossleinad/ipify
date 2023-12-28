import json
import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def help_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""```
        Commands:
        /echo - Echo your message
        /help - Show this help message
        /ipify - Get the bot's public IP address
        /ping - pong
        /start - Welcome message
        ```""",
        parse_mode="Markdown"
    )


async def ipify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in json.loads(os.getenv("ALLOWED_SU_IDS")):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Access denied!")
        return

    ip_address = requests.get('https://icanhazip.com').text.rstrip('\n')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'```{ip_address}```', parse_mode="Markdown")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pong")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


if __name__ == '__main__':
    load_dotenv()
    application = ApplicationBuilder().token(os.getenv("API_KEY")).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    help_handler = CommandHandler('help', help_message)
    ipify_handler = CommandHandler('ipify', ipify)
    ping_handler = CommandHandler('ping', ping)
    start_handler = CommandHandler('start', start)

    application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(ipify_handler)
    application.add_handler(start_handler)
    application.add_handler(ping_handler)

    application.run_polling()