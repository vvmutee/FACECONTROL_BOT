import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Конфигурация
BOT_TOKEN = "..."
CHANNEL_USERNAME = "@test_my_chennel"
ADMIN_ID = 1234567890

MESSAGES = {
    'start': "Привет! Для доступа к контенту подпишись на канал {channel}.",
    'not_subscribed': "❌ Вы не подписаны на канал! Подпишитесь и попробуйте снова.",
    'success': "🎉 Спасибо за подписку! Ваш доступ: https://example.com/secret-content",
    'admin_help': "Используйте /setmessage <ключ> <текст> для изменения сообщений."
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        MESSAGES['start'].format(channel=CHANNEL_USERNAME)
    )


async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        chat_member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )
        status = chat_member.status
        if status in ["member", "administrator", "creator"]:
            await update.message.reply_text(MESSAGES['success'])
        else:
            await update.message.reply_text(MESSAGES['not_subscribed'])
    except Exception as e:
        await update.message.reply_text("Ошибка проверки подписки. Сообщите администратору.")


async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Недостаточно прав!")
        return

    if len(context.args) < 2:
        await update.message.reply_text(MESSAGES['admin_help'])
        return

    key = context.args[0].lower()
    if key not in MESSAGES:
        await update.message.reply_text(MESSAGES['admin_help'])
        return

    new_text = ' '.join(context.args[1:])
    MESSAGES[key] = new_text
    await update.message.reply_text(f"Сообщение {key} обновлено!")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setmessage", set_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_subscription))

    application.run_polling()


if __name__ == '__main__':
    main()
