import os
import logging
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def main_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("ℹ️ О нас", callback_data="about"),
        types.InlineKeyboardButton("💰 Пополнить баланс", callback_data="deposit"),
        types.InlineKeyboardButton("🛒 Товары", callback_data="products")
    )
    return keyboard

def back_button():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("« Назад", callback_data="back")
    )

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("👋 Привет! Выбери раздел:", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == 'back')
async def go_back(callback: types.CallbackQuery):
    await callback.message.edit_text("👋 Главное меню:", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == 'about')
async def about(callback: types.CallbackQuery):
    text = "ℹ️ <b>О нас</b>\n\nМы продаем цифровые товары.\n📞 Поддержка: @support"
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'deposit')
async def deposit(callback: types.CallbackQuery):
    text = "💰 <b>Пополнение</b>\n\nНапиши @admin для пополнения вручную."
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'products')
async def products(callback: types.CallbackQuery):
    text = "🛒 <b>Товары</b>\n\n1. Товар #1 — 100₽\n2. Товар #2 — 250₽\n\nПиши @manager"
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

