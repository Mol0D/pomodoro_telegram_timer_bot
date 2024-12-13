from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def send_message(update: Update, context: CallbackContext) -> None:
    # Send a message and store its message_id
    sent_message = update.message.reply_text("This is the original message.")

    # Store the chat ID and message ID to update later
    context.user_data['chat_id'] = sent_message.chat_id
    context.user_data['message_id'] = sent_message.message_id


# Command to edit the last message
def edit_last_message(update: Update, context: CallbackContext) -> None:
    chat_id = context.user_data.get('chat_id')
    message_id = context.user_data.get('message_id')

    if chat_id and message_id:
        # Edit the previously sent message
        context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="This is the updated message!"
        )
    else:
        update.message.reply_text("No message to edit!")