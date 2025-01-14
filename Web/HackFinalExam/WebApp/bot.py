from telebot import *
import WebApp.config as config
from .models import *

#decorators to filter messages and types
def group_only(func):
    def wrapper(message):
        if message.chat.type in ['group', 'supergroup']:
            return func(message)
    return wrapper
def reply_to_bot_only(func):
    def wrapper(message):
        if message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id:
            return func(message)
    return wrapper

#initializing bot
bot = TeleBot(config.BOT_TOKEN,threaded=False,parse_mode='HTML')
bot.remove_webhook()
# bot.set_webhook(
#     config.WEBHOOK_URL
# )

@bot.message_handler(commands=['start'])
@group_only
def BotCall_Command_Start(message):
    info = Info.objects.last()
    if info.no_group:
        bot.reply_to(
            message,f"Telegramda Guruh ID raqami: <b>{message.chat.id}</b>"
        )

@bot.message_handler(content_types=['text'])
@group_only
@reply_to_bot_only
def BotCall_Got_Answer(message):
    info = Info.objects.last()
    answer = message.text
    try:
        question = Question.objects.get(message_id=message.reply_to_message.message_id)
        question.answer = answer
        question.is_answered = True
        question.save()
        bot.edit_message_text(f"<i>Javob berildi✅</i>",chat_id=info.telegram_group,message_id=question.message_id)
    except:pass
