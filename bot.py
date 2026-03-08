from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="ℹ️ О нас", callback_data="about")
    builder.button(text="💰 Пополнить баланс", callback_data="deposit")
    builder.button(text="🛒 Товары", callback_data="products")
    builder.adjust(1)
    return builder.as_markup()

def back_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="« Назад", callback_data="back")
    return builder.as_markup()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("👋 Привет! Выбери раздел:", reply_markup=main_menu())

@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.edit_text("👋 Главное меню:", reply_markup=main_menu())

@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    text = "ℹ️ <b>О нас</b>\n\nМы продаем цифровые товары.\n📞 Поддержка: @support"
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

@router.callback_query(F.data == "deposit")
async def deposit(callback: CallbackQuery):
    text = "💰 <b>Пополнение</b>\n\nНапиши @admin для пополнения вручную."
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

@router.callback_query(F.data == "products")
async def products(callback: CallbackQuery):
    text = "🛒 <b>Товары</b>\n\n1. Товар #1 — 100₽\n2. Товар #2 — 250₽\n\nПиши @manager"
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
