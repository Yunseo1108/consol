import telebot  
from config import token  
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi! I am a chat moderation bot.")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:  # The /ban command should be a reply
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status

        if user_status in ['administrator', 'creator']:
            bot.reply_to(message, "You can't ban an administrator.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"User @{message.reply_to_message.from_user.username} has been banned.")
    else:
        bot.reply_to(message, "You must reply to a user's message to ban them.")

@bot.message_handler(func=lambda message: True)
def check_and_ban_links(message):
    if message.text and "https://" in message.text:
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status

        if user_status in ['administrator', 'creator']:
            bot.reply_to(message, "You can't ban administrators!")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"User @{message.from_user.username} has been banned for sending a link.")


bot.infinity_polling(none_stop=True)