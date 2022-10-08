import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from dotenv import load_dotenv

from web3utils import *
from utils import generate_qr_code


load_dotenv("keys.env")
token = str(os.getenv("TELEGRAM_BOT"))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

users = {}
community_name = 'Satoshi' #  Placeholder name for the Community fund


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def link(update, context):
    """Link your ethereum address to your telegram account."""
    update.message.reply_text('Link!')
    update.message.reply_text("<a href='https://www.google.com/'>Google</a>")
    update.message.reply_text("<a href='tg://user?id=123456789'>Link</a>")

def start(update, context):
    """Start the bot."""
    update.message.reply_text('GM! Welcome to the community fund bot.')
    update.message.reply_text('Please create your community fund using the command /create_fund <name of fund>')

def create_fund(update, context):
    """Setup the community fund when the command /create_fund is issued."""
    try:
        community_name = update.message.text.split(' ')[1]
        update.message.reply_text('GM! New community fund created: ' + community_name)
        txn = build_create_community_tx(community_name)
        update.message.reply_text('Create Fund Call Data: ' + txn)
    except:
        logger.warning('Update "%s" caused error "%s"', update, context.error)
        update.message.reply_text('Please provide a community name.')
        update.message.reply_text('Example: /create_fund Satoshi')


def help(update, context):
    """Send all commands when the command /help is issued."""
    update.message.reply_text(
    '''
    /start - Start the bot
    /create_fund <community name> - Start the bot
    /register - Register your ethereum address
    /lend <amount> - Lend money to the community fund
    /borrow <amount> - Borrow money from the community fund
    /repay <amount> - Repay money to the community fund
    /withdraw <amount> - Withdraw money from the community fund
    /balance - Check your balance
    /help - Show all commands
    ''')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def register(update, context):
    """Register a new user."""
    # check if user is already registered
    if update.message.from_user.id in users:
        update.message.reply_text('You are already registered!')
        return

    update.message.reply_text('Registering new user into community fund.')
    txn = build_join_community_tx()
    update.message.reply_text('Join Community Call Data: ' + txn)

    # Generate Qr code
    img = generate_qr_code(txn)

    # send image to user
    update.message.reply_photo(img)

   

def get_users(update,context):
    update.message.reply_text(users)


def lend(update, context):
    """Provide money for the community fund."""
    update.message.reply_text('Lend!')
    try: 
        # get user's input and save it to a variable
        amount = update.message.text.split(' ')[1]
        build_deposit_tx(amount)
        update.message.reply_text('Lent ' + amount + ' to the community fund.')
    except:
        update.message.reply_text('Please provide a valid amount.')
        update.message.reply_text('Example: /lend 100')

    

def borrow(update, context):
    """Borrow money from the community fund."""
    update.message.reply_text('Borrow!')
    try:
        # get user's input and save it to a variable
        amount = update.message.text.split(' ')[1]
        build_withdraw_tx(amount)
        update.message.reply_text('Borrowed ' + amount + ' from the community fund.')
    except:
        update.message.reply_text('Please provide a valid amount.')
        update.message.reply_text('Example: /borrow 100')

def repay(update, context):
    """Repay money to the community fund."""
    update.message.reply_text('Repay!')
    try:
        # get user's input and save it to a variable
        amount = update.message.text.split(' ')[1]
        build_deposit_tx(amount)
        update.message.reply_text('Repaid ' + amount + ' to the community fund.')
    except:
        update.message.reply_text('Please provide a valid amount.')
        update.message.reply_text('Example: /repay 100')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("link", link))
    dp.add_handler(CommandHandler("create_fund", create_fund))
    dp.add_handler(CommandHandler("register", register))

    dp.add_handler(CommandHandler("lend", lend))
    dp.add_handler(CommandHandler("borrow", borrow))
    dp.add_handler(CommandHandler("repay", repay))
    dp.add_handler(CommandHandler("get_users", get_users))

    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()