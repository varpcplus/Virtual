import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")],
        [InlineKeyboardButton("💰 Пополнить баланс", callback_data="deposit")],
        [InlineKeyboardButton("🛒 Товары", callback_data="products")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("« Назад", callback_data="back")]])

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Привет! Выбери раздел:", reply_markup=main_menu())

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "back":
        query.edit_message_text("👋 Главное меню:", reply_markup=main_menu())
    elif query.data == "about":
        text = "ℹ️ О нас\n\nМы продаем цифровые товары.\n📞 Поддержка: @support"
        query.edit_message_text(text, reply_markup=back_button())
    elif query.data == "deposit":
        text = "💰 Пополнение\n\nНапиши @admin для пополнения вручную."
        query.edit_message_text(text, reply_markup=back_button())
    elif query.data == "products":
        text = "🛒 Товары\n\n1. Товар #1 — 100₽\n2. Товар #2 — 250₽\n\nПиши @manager"
        query.edit_message_text(text, reply_markup=back_button())

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
