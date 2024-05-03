import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove

from markups import get_sale_button, get_yes_or_no_markup, get_contacts_markup

token = '6072367589:AAHYBuFZDP1MD3MhKQUn0YbU4ChEWKFCBP0'
bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()


class CollectionStates(StatesGroup):
    phone_and_name = State()


@dp.message(CommandStart())
async def start(msg: Message):
    text = ('Добрый день! Я рад приветствовать вас в моей практике, где я '
            'специализируюсь на работе с отношениями и помощи в преодолении травмы. '
            'В жизни каждого из нас могут возникать сложные ситуации, '
            'которые оставляют следы и вызывают эмоциональные и психологические травмы. '
            'Моя задача - помочь вам исцелиться и восстановить гармонию внутри '
            'себя и в отношениях с другими людьми. Я предлагаю индивидуальный '
            'подход и эффективные методы, основанные на современных психологических '
            'техниках и терапии травмы. Вместе мы будем искать ресурсы внутри вас, '
            'чтобы вы смогли справиться с трудностями и построить здоровые и крепкие '
            'отношения. Не стесняйтесь обратиться ко мне - вашему психологу, '
            'готовому поддержать вас на этом пути к исцелению и росту.')
    await asyncio.sleep(1)
    message = await bot.send_message(msg.from_user.id, text)
    await bot.pin_chat_message(msg.from_user.id, message.message_id)

    file_id = 'BAACAgIAAxkDAAN2ZRFs-xOTow0PJRmvSciarDMUtfgAArsyAALO0ZFIS2nNT3TqY6owBA'
    try:
        await bot.send_video(msg.from_user.id, file_id,
                             caption='Для получения купона жми на кнопку, и действиуй инструкциям!',
                             reply_markup=get_sale_button().as_markup())
    except Exception:
        await bot.send_video(msg.from_user.id, FSInputFile('IMG_0287.MP4'),
                             caption='Для получения купона жми на кнопку, и действиуй инструкциям!',
                             reply_markup=get_sale_button().as_markup())


@dp.callback_query(lambda call: call.data == 'get_sale')
async def get_sale(call: CallbackQuery, state: FSMContext):
    await state.update_data(username=call.from_user.username)
    await state.set_state(CollectionStates.phone_and_name)
    await bot.send_message(call.from_user.id, "Отправьте свой номер телефона, и как к вам можно обращаться")


@dp.message(CollectionStates.phone_and_name)
async def verify_phone(msg: Message, state: FSMContext):
    await state.update_data(phone_and_name=msg.text)
    await bot.send_message(msg.from_user.id, "С вами можно связаться по номеру который вы прислали?",
                           reply_markup=get_yes_or_no_markup('phone').as_markup())


@dp.callback_query(lambda call: call.data.count('verify'))
async def verify(call: CallbackQuery, state: FSMContext):
    await call.answer()

    if call.data.count('no'):
        await bot.send_message(
            call.from_user.id,
            "Напишите ваш номер телефона без 8 в начале!\n\n"
            "Неправильно: 89857772244.\nПравильно: 9857772244, 79857772244, или +79857772244.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    elif call.data.count('yes'):
        await send_coupon(call, state)


async def send_coupon(call: CallbackQuery, state: FSMContext):
    url = ('https://sun9-10.userapi.com/impg/WVIjFPzp6vjGEiwMAJ49pkksvLda87VWS_5wJg/MZb_ZlCITOU.jpg?'
           'size=1280x651&quality=96&sign=2d907db2e74dba8c90bc682931a5045e&c_uniq_tag='
           'EwCi3kuJj4cKCZy9yJKoI29sOlqR1W6sL8baxuGyk9U&type=album')
    await bot.send_photo(call.from_user.id, url, caption='Вы получили купон на скидку в 30%, скоро с вами свяжуться!')

    admin_id = 1265295134
    data_state = await state.get_data()

    telegram_url = f'https://t.me/{data_state["username"]}'
    whatsapp_url = f'https://wa.me/{data_state["phone_and_name"]}'
    text = (f"<b>Пользователь получил купон:</b>\n\n"
            f"<b>Номер телефона и имя:</b> {data_state['phone_and_name']}")

    mp = get_contacts_markup(telegram_url=telegram_url, whatsapp_url=whatsapp_url).as_markup()
    await bot.send_message(admin_id, text, reply_markup=mp)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
