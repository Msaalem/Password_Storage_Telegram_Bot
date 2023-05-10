import telegram
from telegram.ext import *
import time

# Dictionary to store passwords for each user
passwords = {}

# Define the /set command handler
def set_password(update, context):
    chat_id = update.message.chat_id
    args = context.args
    if len(args) != 2:
        context.bot.send_message(chat_id=chat_id, text='Usage: /set <service> <password>')
        return
    service, password = args
    passwords.setdefault(chat_id, {})[service] = password
    context.bot.send_message(chat_id=chat_id, text=f'Password for {service} set successfully!')

# Define the /get command handler
def get_password(update, context):
    chat_id = update.message.chat_id
    args = context.args
    if len(args) != 1:
        context.bot.send_message(chat_id=chat_id, text='Usage: /get <service>')
        return
    service = args[0]
    if chat_id in passwords and service in passwords[chat_id]:
        password = passwords[chat_id][service]
        # Delete the password after 10 seconds to ensure security
        context.bot.send_message(chat_id=chat_id, text=f'Password for {service}: {password}')
        time.sleep(10)
        context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    else:
        context.bot.send_message(chat_id=chat_id, text=f'No password found for {service}')

# Define the /del command handler
def delete_password(update, context):
    chat_id = update.message.chat_id
    args = context.args
    if len(args) != 1:
        context.bot.send_message(chat_id=chat_id, text='Usage: /del <service>')
        return
    service = args[0]
    if chat_id in passwords and service in passwords[chat_id]:
        del passwords[chat_id][service]
        context.bot.send_message(chat_id=chat_id, text=f'Password for {service} deleted successfully!')
    else:
        context.bot.send_message(chat_id=chat_id, text=f'No password found for {service}')

# Define the main function to run the bot
def main():
    # Create a Telegram bot object
    bot = telegram.Bot(token='5943369949:AAFi77mhmvzKFKSN0JwhP7O99TTLWj5VvIc')

    # Create an updater object to receive updates from Telegram
    updater = Updater(bot.token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the command handlers
    dp.add_handler(CommandHandler('set', set_password))
    dp.add_handler(CommandHandler('get', get_password))
    dp.add_handler(CommandHandler('del', delete_password))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Call the main function to run the bot
if __name__ == '__main__':
    main()
