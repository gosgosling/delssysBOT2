import os
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv('BOT_TOKEN')

def delete_system_messages(update: Update, context: CallbackContext):
    """Удаляет системные сообщения в группах"""
    
    # Проверяем, что сообщение из группы
    if not update.effective_chat.type in ['group', 'supergroup']:
        return
    
    # Проверяем, что у бота есть права на удаление сообщений
    bot_member = context.bot.get_chat_member(
        update.effective_chat.id, 
        context.bot.id
    )
    
    if not bot_member.can_delete_messages:
        return
    
    message = update.message
    
    # Системные сообщения обычно не имеют отправителя (from_user = None)
    # или имеют специальные типы
    if (message.from_user is None or 
        message.new_chat_members or 
        message.left_chat_member or
        message.new_chat_title or
        message.new_chat_photo or
        message.delete_chat_photo or
        message.group_chat_created or
        message.supergroup_chat_created or
        message.channel_chat_created or
        message.message_auto_delete_timer_changed or
        message.pinned_message):
        
        try:
            message.delete()
            logger.info(f"Удалено системное сообщение в чате {update.effective_chat.id}")
        except Exception as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

def start(update: Update, context: CallbackContext):
    """Обработчик команды /start"""
    update.message.reply_text(
        "Привет! Я бот для удаления системных сообщений в группах. "
        "Добавьте меня в группу и дайте права на удаление сообщений."
    )

def main():
    """Запуск бота"""
    if not TOKEN:
        logger.error("Не установлен BOT_TOKEN!")
        return
    
    # Создаем updater
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Добавляем обработчики
    dispatcher.add_handler(MessageHandler(Filters.all, delete_system_messages))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() 