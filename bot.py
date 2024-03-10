import telebot
from extentions import CurrencyConverter, APIException
from configbot import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def handle_start_help(message):
    instructions = (
        "Welcome to the Currency Converter Bot!\n"
        "To use this bot, send a message in the format:\n"
        "<base_currency> <quote_currency> <amount>\n"
        "For example: USD EUR 100\n"
        "You can also use the /values command to see available currencies."
    )
    bot.reply_to(message, instructions)


@bot.message_handler(commands=["values"])
def handle_values(message):
    available_currencies = ["USD", "EUR", "GBP", "JPY", "CAD"]  
    currencies_text = "\n".join(available_currencies)
    bot.reply_to(message, f"Available currencies:\n{currencies_text}")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        input_text = message.text.upper().split()
        if len(input_text) != 3:
            raise APIException("Invalid input. Please use the format: <base_currency> <quote_currency> <amount>")

        base_currency, quote_currency, amount = input_text
        amount = float(amount)

        converted_amount = CurrencyConverter.get_price(base_currency, quote_currency, amount)
        bot.reply_to(message, f"{amount:.2f} {base_currency} = {converted_amount:.2f} {quote_currency}")
    except APIException as e:
        bot.reply_to(message, f"Error: {e.message}")


bot.polling()
