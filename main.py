import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from dotenv import load_dotenv
from tele_bot import bot
from web3utils import *
from utils import generate_qr_code
from telegram import ParseMode
from credit_score import get_credit_score


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
    bot.send_message(update.effective_message.chat_id,'Link!')
    bot.send_message(update.effective_message.chat_id,"<a href='https://www.google.com/'>Google</a>", parse_mode=ParseMode.HTML)

def start(update, context):
    """Start the bot."""
    chat_id = update.effective_message.chat_id
    bot.send_message(chat_id,
    '''
    Welcome to the Community Fund Bot Decoop!
    Step 1: Create your community fund using the command /create_fund <name of fund>
    Step 2: Register users ethereum address using the command /register
    Step 3: Lend money to the community fund using the command /lend <amount>
    Step 4: Borrow money from the community fund using the command /borrow <amount>
    Step 5: Repay money to the community fund using the command /repay <amount>
    Step 6: Withdraw money from the community fund using the command /withdraw <amount>
    Step 7: Check your balance using the command /balance <address>
    Step 8: Check your credit score using the command /credit_score <address>
    ''')
   

def create_fund(update, context):
    """Setup the community fund when the command /create_fund is issued."""
    try:
        community_name = update.message.text.split(' ')[1]
        bot.send_message(update.message.chat_id, 'GM! Creating new community fund: ' + community_name)
        mobile_link,desktop_link = build_create_community_tx(community_name)
        bot.send_message(update.message.chat_id, f"Create Community URL :")
        bot.send_message(update.message.chat_id, f"Mobile Link: {mobile_link}")
        bot.send_message(update.message.chat_id, f"Desktop Link: {desktop_link}")
    
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
    /balance <address> - Check your balance
    /credit_score <address> - Check your credit score
    /get_users - Get all users
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

    bot.send_message(update.message.chat_id,'Registering new user into community fund.')
    mobile_link,desktop_link = build_join_community_tx()
    bot.send_message(update.message.chat_id,f"Register URL:")
    bot.send_message(update.message.chat_id,f"Mobile Link: {mobile_link}")
    bot.send_message(update.message.chat_id,f"Desktop Link: {desktop_link}")

    # Generate Qr code
    img = generate_qr_code(mobile_link)
    f = open('qr.png', 'rb')

    # send image to user
    bot.sendPhoto(photo=f, chat_id=update.message.chat_id)
   

def get_users(update,context):
    update.message.reply_text(users)


def lend(update, context):
    """Provide money for the community fund."""
    update.message.reply_text(f'{update.message.from_user.first_name} is lending money to the community fund.')
    try: 
        # get user's input and save it to a variable
        amount = update.message.text.split(' ')[1]
        logger.info(amount)
        mobile_link,desktop_link = build_deposit_tx(amount)
        # bot.send_message(update.message.chat_id, f"<a href={txn}>Lend {amount} </a>", parse_mode=ParseMode.HTML)
        bot.send_message(update.message.chat_id, f"Lend {amount} URL:")
        bot.send_message(update.message.chat_id, f"Mobile Link: {mobile_link}")
        bot.send_message(update.message.chat_id, f"Desktop Link: {desktop_link}")

        
    except:
        bot.send_message(update.message.chat_id, 'Please provide an amount.')
        bot.send_message(update.message.chat_id, 'Example: /lend 1000')
    

def borrow(update, context):
    """Borrow money from the community fund."""
    update.message.reply_text('Borrow!')
    try:
        # get user's input and save it to a variable
        amount = update.message.text.split(' ')[1]
        mobile_link,desktop_link = build_withdraw_tx(amount)
        # bot.send_message(update.message.chat_id, f"<a href={txn}>Borrow {amount} </a>", parse_mode=ParseMode.HTML)
        bot.send_message(update.message.chat_id, f"Borrow {amount} URL:")
        bot.send_message(update.message.chat_id, f"Mobile Link: {mobile_link}")
        bot.send_message(update.message.chat_id, f"Desktop Link: {desktop_link}")

    except:
        bot.send_message(update.message.chat_id, 'Please provide a valid amount.')
        bot.send_message(update.message.chat_id, 'Example: /borrow 100')

def repay(update, context):
    """Repay money to the community fund."""
    bot.send_message(update.message.chat_id, f'{update.message.from_user.first_name} is repaying money to the community fund.')
    try:
        # get user's input and save it to a variable
        amount = update.message.text.split(' ')[1]
        mobile_link,desktop_link = build_deposit_tx(amount)
        # bot.send_message(update.message.chat_id,f"<a href={txn}>Repay {amount} </a>", parse_mode=ParseMode.HTML)
        bot.send_message(update.message.chat_id,f"Repay {amount} URL:")
        bot.send_message(update.message.chat_id,f"Mobile Link: {mobile_link}")
        bot.send_message(update.message.chat_id,f"Desktop Link: {desktop_link}")

    except:
        bot.send_message(update.message.chat_id,'Please provide a valid amount.', )
        bot.send_message(update.message.chat_id, 'Example: /repay 100')

def withdraw(update, context):
    """Withdraw money from the community fund."""
    bot.send_message(update.message.chat_id, f'{update.message.from_user.first_name} is withdrawing money from the community fund.')
    try:
        # get user's input and save it to a variable
        amount = update.message.text.split(' ')[1]
        mobile_link,desktop_link = build_withdraw_tx(amount)
        # bot.send_message(update.message.chat_id,f"<a href={txn}>Withdraw {amount} </a>", parse_mode=ParseMode.HTML)
        bot.send_message(update.message.chat_id,f"Withdraw {amount} URL:")
        bot.send_message(update.message.chat_id,f"Mobile Link: {mobile_link}")
        bot.send_message(update.message.chat_id,f"Desktop Link: {desktop_link}")

    except:
        bot.send_message(update.message.chat_id,'Please provide a valid amount.')
        bot.send_message(update.message.chat_id, 'Example: /withdraw 100')

def balance(update, context):
    """Check your balance."""
    bot.send_message(update.message.chat_id, f'Checking balance for {update.message.from_user.first_name}')
    try:
        # get user's input and save it to a variable
        address = update.message.text.split(' ')[1]
        balance = get_erc20_balance(address)
        bot.send_message(update.message.chat_id, f"Your balance is {balance} ")
    except:
        bot.send_message(update.message.chat_id,'Please provide a valid address.')
        bot.send_message(update.message.chat_id, 'Example: /balance 0x1234567890')

def credit_score(update, context):
    update.message.reply_text(f'Getting Credit Score for {update.message.from_user.first_name}')
    try:
        # get user's input and save it to a variable
        address = update.message.text.split(' ')[1]
        score = get_credit_score(address)
        bot.send_message(update.message.chat_id, f"Your credit score is {score} ")
    except:
        bot.send_message(update.message.chat_id,'Please provide a valid address.')
        bot.send_message(update.message.chat_id, 'Example: /credit_score 0x1234567890')


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
    dp.add_handler(CommandHandler("withdraw", withdraw))

    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("credit_score", credit_score))

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