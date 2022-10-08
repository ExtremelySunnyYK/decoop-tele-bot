import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv


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
def start(update, context):
    """Send a message when the command /start is issued."""
    try:
        community_name = update.message.text.split(' ')[1]
        update.message.reply_text('GM! New community fund created: ' + community_name)
    except:
        update.message.reply_text('GM! Welcome to the community fund.')


def help(update, context):
    """Send all commands when the command /help is issued."""
    update.message.reply_text('''
    /start <community name> - Start the bot
    /register <address> - Register your ethereum address
    /lend - Lend money to the community fund
    /borrow - Borrow money from the community fund
    /repay - Repay money to the community fund
    /withdraw - Withdraw money from the community fund
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

    try:
        # get user's input and save it to a variable
        address = update.message.text.split(' ')[1]

        # get user telegram id
        user_id = update.message.from_user.first_name

        # store ethereum address and telegram id in a dictionary
        users[user_id] = address

        # send back the user's input
        update.message.reply_text('Registered new user: ' + user_id + ' with address: ' + address)

        # Mint a SBT for the user
        
    except:
        update.message.reply_text('Please provide a valid ethereum address.')
        update.message.reply_text('Example: /register 0x1234567890abcdef1234567890abcdef12345678')

def get_users(update,context):
    update.message.reply_text(users)


def lend(update, context):
    """Provide money for the community fund."""
    update.message.reply_text('Lend!')

def borrow(update, context):
    """Borrow money from the community fund."""
    update.message.reply_text('Borrow!')

def repay(update, context):
    """Repay money to the community fund."""
    update.message.reply_text('Repay!')


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