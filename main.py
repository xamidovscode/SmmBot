import sys
from aiogram import Bot, Dispatcher, types, Router
import asyncio
import logging
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
support_token = '7957119245:AAHd5s9tC74mp8Krbs8CuGZ250qfGGPPOC0'
channel_id = '@soffcrm'  # Kanal username'ni kiriting (masalan, '@your_channel')

bot = Bot(token=support_token)
dp = Dispatcher()
router = Router()

# CallbackData yaratish

async def check_subscription(user_id):
    """Foydalanuvchini kanalga obuna bo'lganligini tekshiradi"""
    member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    return member.status in ['member', 'administrator', 'creator']

@router.message(CommandStart())
async def start_command_handler(message: types.Message):
    chat_id = message.from_user.id

    # Inline keyboard yaratish: obuna bo'lish uchun kanalga havola va tekshirish tugmasi
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="SoffCRM", url=f"https://t.me/{channel_id[1:]}")],
            [InlineKeyboardButton(text="✅TEKSHIRISH", callback_data='check_subscription')]
        ]
    )

    await message.answer(f"Salom! Iltimos kanaliga obuna bo'ling", reply_markup=keyboard)


import os
FILE_PATH = 'subscribed.txt'


async def save_user_id(user_id):
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            user_ids = f.read().splitlines()
    else:
        user_ids = []

    if str(user_id) not in user_ids:
        with open(FILE_PATH, 'a') as f:
            f.write(f"{user_id}\n")


@router.callback_query(F.data == "check_subscription")
async def check_subscription_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        file_path = "qollanma.pdf"
        input_file = FSInputFile(file_path)
        await save_user_id(user_id)
        await bot.send_message(chat_id=user_id, text="Obuna uchun rahmat!🥳🥳🥳")
        await bot.send_document(chat_id=user_id, document=input_file, caption="Bonus Qo'llanma 🎁\n\nO'quv Markazlar Bankrot Bo'lishiga Sabab Bo'ladigan Top 3 ta Xato")
    else:
        await bot.send_message(chat_id=user_id, text=f"Siz hali kanalga obuna bo'lmagansiz. Iltimos, obuna bo'ling.")
    await callback_query.answer()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
