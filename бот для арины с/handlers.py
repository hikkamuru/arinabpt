import os
import random
import datetime
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import HER_NAME, HIS_NAME, PHOTOS_DIR

router = Router()


class DateStates(StatesGroup):
    waiting_for_action = State()


LOCATIONS = [
    "☕ Уютная кофейня",
    "🌳 Парк",
    "🎭 Что-то необычное"
]


def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Выбрать локацию", callback_data="choose_location")],
        [InlineKeyboardButton(text="👗 Дресс-код", callback_data="dress_code")],
        [InlineKeyboardButton(text="😘 Секретный бонус", callback_data="secret_bonus")],
        [InlineKeyboardButton(text="🎫 Билет на свидание", callback_data="ticket")],
    ])


def get_location_keyboard() -> InlineKeyboardMarkup:
    builder = []
    for i, loc in enumerate(LOCATIONS):
        builder.append([InlineKeyboardButton(text=loc, callback_data=f"location_{i}")])
    builder.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=builder)


def get_random_photo() -> str | None:
    photos = [f for f in os.listdir(PHOTOS_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
    if photos:
        return os.path.join(PHOTOS_DIR, random.choice(photos))
    return None


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    photo = get_random_photo()
    
    greeting = f"❤️ Привет, {HER_NAME}! ❤️\n\n"
    greeting += "Добро пожаловать в <b>Менеджер свидания</b>!\n\n"
    greeting += "Давай выберем идеальную конфигурацию нашего вечера:"
    
    if photo:
        await message.answer_photo(
            photo=photo,
            caption=greeting,
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(greeting, reply_markup=get_main_keyboard())
    
    await state.set_state(DateStates.waiting_for_action)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback, state: FSMContext):
    photo = get_random_photo()
    
    text = f"❤️ {HER_NAME}, ты снова со мной! ❤️\n\nВыбирай, что хочешь узнать:"
    
    if photo:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=get_main_keyboard()
        )
    else:
        await callback.message.edit_text(text, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "choose_location")
async def choose_location(callback, state: FSMContext):
    text = f"🌟 {HER_NAME}, выбери локацию для нашего свидания:\n\n"
    for loc in LOCATIONS:
        text += f"• {loc}\n"
    
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_location_keyboard()
    )


@router.callback_query(F.data.startswith("location_"))
async def select_location(callback, state: FSMContext):
    idx = int(callback.data.split("_")[1])
    location = LOCATIONS[idx]
    
    photo = get_random_photo()
    text = f"✨ Отличный выбор! ✨\n\n"
    text += f"📍 <b>{location}</b>\n\n"
    text += "Жду тебя с нетерпением! 🫶"
    
    if photo:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=get_main_keyboard()
        )
    else:
        await callback.message.edit_text(text, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "dress_code")
async def dress_code(callback, state: FSMContext):
    photo = get_random_photo()
    
    text = f"👗 {HER_NAME}, по дресс-коду:\n\n"
    text += "Надень то, в чём тебе удобно, милая!\n\n"
    text += "💫 Я все равно буду смотреть только в твои глаза 💫"
    
    if photo:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=get_main_keyboard()
        )
    else:
        await callback.message.edit_text(text, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "secret_bonus")
async def secret_bonus(callback, state: FSMContext):
    photo = get_random_photo()
    
    text = f"😘 <b>Секретный бонус!</b>\n\n"
    text += f"{HER_NAME}, теперь при встрече ты <b>обязана</b> поцеловать меня в щёчку! 💋\n\n"
    text += "Это не обсуждается! 🫣"
    
    if photo:
        await callback.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=text),
            reply_markup=get_main_keyboard()
        )
    else:
        await callback.message.edit_text(text, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "ticket")
async def send_ticket(callback, state: FSMContext):
    photo = os.path.join(PHOTOS_DIR, "1.jpg")
    
    now = datetime.datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    time_str = (now + datetime.timedelta(hours=3)).strftime("%H:%M")
    
    text = f"""🎫 <b>БИЛЕТ НА СВИДАНИЕ</b> 🎫

━━━━━━━━━━━━━━━━━━━━━
👤 <b>{HER_NAME}</b> & <b>{HIS_NAME}</b>
━━━━━━━━━━━━━━━━━━━━━

📅 Дата: {date_str}
⏰ Время: {time_str}
📍 Место: Сюрприз!

━━━━━━━━━━━━━━━━━━━━━

❤️ Это будет незабываемый вечер!
❤️ Жду тебя, моя хорошая!

━━━━━━━━━━━━━━━━━━━━━"""

    await callback.message.answer_photo(
        photo=photo,
        caption=text
    )
    
    text2 = f"✨ {HER_NAME}, теперь ты готова к свиданию! ✨\n\nЖду тебя! 🫶"
    await callback.message.answer(text2, reply_markup=get_main_keyboard())
