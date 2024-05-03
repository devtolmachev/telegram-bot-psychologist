from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, KeyboardBuilder


def get_sale_button() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    btn = InlineKeyboardButton(text='Получить скидку', callback_data='get_sale')
    kb.add(btn)
    return kb


def get_yes_or_no_markup(item: str) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='Да', callback_data=f'verify_{item}_yes')
    btn2 = InlineKeyboardButton(text='Нет', callback_data=f'verify_{item}_no')
    kb.add(btn1, btn2)
    return kb


def get_contacts_markup(telegram_url: str, whatsapp_url: str) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text="Telegram", url=telegram_url)
    btn2 = InlineKeyboardButton(text="Whatsapp", url=whatsapp_url)

    kb.add(btn1, btn2)
    return kb
