import telebot
from pytonlib import TonlibClient
import asyncio

bot = telebot.TeleBot('<your_bot_token>')
client = TonlibClient()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the TON Guessing Game! Send /guess <number> to play.")

@bot.message_handler(commands=['guess'])
def handle_guess(message):
    try:
        guess = int(message.text.split()[1])

        async def check_guess():
            await client.init()
            contract_address = "<contract_address>"
            result = await client.raw_run_contract(
                address=contract_address,
                function_name='guess',
                input={'_guess': guess}
            )
            return result['output']

        result = asyncio.run(check_guess())
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, "Error: " + str(e))

bot.polling()