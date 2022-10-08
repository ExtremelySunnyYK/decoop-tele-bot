# Telegram bot for cooperative banking (decoop)


## Setup
1. Create Virtual Env
```
python3 -m venv venv
```
2. Activate Virtual Env
```
source venv/bin/activate
```
3. Install requirements
```
pip install -r requirements.txt
```
4. Create keys.env file with the following content
```
# Please rename this file to keys.env after filling these

export TELEGRAM_BOT=<your telegram bot token>
export CHAT_ID=<your chat id>
```
5. Run the bot
```
python main.py
```