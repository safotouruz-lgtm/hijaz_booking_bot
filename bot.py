# -*- coding: utf-8 -*-
"""
HIJAZ Booking Bot
- 5 til: O'zbek, Rus, Ingliz, Arab, Turk
- Mehmonxona bron so'rovi (shahar, daraja, taomlanish, mehmon, sana, budjet)
- Transfer so'rovi (aeroport / shaharlararo / ziyorat)
- So'rovlar HIJAZ guruhiga yuboriladi
"""
import asyncio
import logging
import os
import json
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)

from lang import t, TR

# ==================== SOZLAMALAR ====================
BOT_TOKEN = os.getenv("BOT_TOKEN", "BU_YERGA_TOKEN")   # @BotFather beradi
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "0"))  # HIJAZ guruh ID (masalan -1001234567890)
REQUESTS_FILE = "requests.json"                          # so'rovlar tarixi

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

# foydalanuvchi tili (xotirada; server o'chsa tiklanadi — start bosadi)
user_lang = {}

def UL(uid):
    return user_lang.get(uid, "uz")


# ==================== HOLATLAR (FSM) ====================
class Form(StatesGroup):
    service = State()       # mehmonxona/transfer/ikkalasi
    # mehmonxona
    city = State()
    stars = State()
    meal = State()
    guests = State()
    checkin = State()
    checkout = State()
    budget = State()
    # transfer
    tr_type = State()
    tr_route = State()
    tr_date = State()
    tr_pax = State()
    # umumiy
    phone = State()
    name = State()


# ==================== KLAVIATURALAR ====================
def kb_lang():
    kb = [[InlineKeyboardButton(text=TR[l]["lang_name"], callback_data=f"lang:{l}")]
          for l in ["uz", "ru", "en", "ar", "tr"]]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def kb_menu(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "menu_booking"), callback_data="booking")],
        [InlineKeyboardButton(text=t(lang, "menu_contact"), callback_data="contact"),
         InlineKeyboardButton(text=t(lang, "menu_info"), callback_data="info")],
        [InlineKeyboardButton(text=t(lang, "menu_lang"), callback_data="changelang")],
    ])

def kb_service(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "svc_hotel"), callback_data="svc:hotel")],
        [InlineKeyboardButton(text=t(lang, "svc_transfer"), callback_data="svc:transfer")],
        [InlineKeyboardButton(text=t(lang, "svc_both"), callback_data="svc:both")],
    ])

def kb_city(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "city_makkah"), callback_data="city:makkah")],
        [InlineKeyboardButton(text=t(lang, "city_madinah"), callback_data="city:madinah")],
        [InlineKeyboardButton(text=t(lang, "city_both"), callback_data="city:both")],
    ])

def kb_stars(lang):
    rows = [[InlineKeyboardButton(text=f"{n}⭐", callback_data=f"stars:{n}") for n in (3, 4, 5)]]
    rows.append([InlineKeyboardButton(text=t(lang, "stars_any"), callback_data="stars:any")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def kb_meal(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "meal_ro"), callback_data="meal:ro")],
        [InlineKeyboardButton(text=t(lang, "meal_bb"), callback_data="meal:bb")],
        [InlineKeyboardButton(text=t(lang, "meal_hb"), callback_data="meal:hb")],
        [InlineKeyboardButton(text=t(lang, "meal_fb"), callback_data="meal:fb")],
    ])

def kb_skip(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "skip"), callback_data="skip")]
    ])

def kb_transfer_type(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "tr_airport"), callback_data="trt:airport")],
        [InlineKeyboardButton(text=t(lang, "tr_intercity"), callback_data="trt:intercity")],
        [InlineKeyboardButton(text=t(lang, "tr_ziyorat"), callback_data="trt:ziyorat")],
    ])

def kb_phone(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, "phone_btn"), request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True,
    )


# ==================== /START ====================
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(t("uz", "choose_lang"), reply_markup=kb_lang())

@dp.callback_query(F.data.startswith("lang:"))
async def set_lang(cb: CallbackQuery, state: FSMContext):
    lang = cb.data.split(":")[1]
    user_lang[cb.from_user.id] = lang
    await state.clear()
    await cb.message.edit_text(t(lang, "welcome"), reply_markup=kb_menu(lang))
    await cb.answer()

@dp.callback_query(F.data == "changelang")
async def change_lang(cb: CallbackQuery):
    await cb.message.edit_text(t("uz", "choose_lang"), reply_markup=kb_lang())
    await cb.answer()

@dp.callback_query(F.data == "contact")
async def show_contact(cb: CallbackQuery):
    lang = UL(cb.from_user.id)
    await cb.message.answer(t(lang, "contact_txt"))
    await cb.answer()

@dp.callback_query(F.data == "info")
async def show_info(cb: CallbackQuery):
    lang = UL(cb.from_user.id)
    await cb.message.answer(t(lang, "info_txt"))
    await cb.answer()


# ==================== BRON BOSHLASH ====================
@dp.callback_query(F.data == "booking")
async def start_booking(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    await state.set_state(Form.service)
    await cb.message.answer(t(lang, "choose_service"), reply_markup=kb_service(lang))
    await cb.answer()

@dp.callback_query(Form.service, F.data.startswith("svc:"))
async def choose_service(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    svc = cb.data.split(":")[1]  # hotel/transfer/both
    await state.update_data(service=svc)
    if svc in ("hotel", "both"):
        await state.set_state(Form.city)
        await cb.message.answer(t(lang, "choose_city"), reply_markup=kb_city(lang))
    else:  # faqat transfer
        await state.set_state(Form.tr_type)
        await cb.message.answer(t(lang, "transfer_type"), reply_markup=kb_transfer_type(lang))
    await cb.answer()


# ==================== MEHMONXONA OQIMI ====================
@dp.callback_query(Form.city, F.data.startswith("city:"))
async def choose_city(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    await state.update_data(city=cb.data.split(":")[1])
    await state.set_state(Form.stars)
    await cb.message.answer(t(lang, "hotel_stars"), reply_markup=kb_stars(lang))
    await cb.answer()

@dp.callback_query(Form.stars, F.data.startswith("stars:"))
async def choose_stars(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    await state.update_data(stars=cb.data.split(":")[1])
    await state.set_state(Form.meal)
    await cb.message.answer(t(lang, "meal"), reply_markup=kb_meal(lang))
    await cb.answer()

@dp.callback_query(Form.meal, F.data.startswith("meal:"))
async def choose_meal(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    await state.update_data(meal=cb.data.split(":")[1])
    await state.set_state(Form.guests)
    await cb.message.answer(t(lang, "guests"))
    await cb.answer()

@dp.message(Form.guests)
async def input_guests(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    if not message.text.strip().isdigit():
        await message.answer(t(lang, "invalid_num"))
        return
    await state.update_data(guests=message.text.strip())
    await state.set_state(Form.checkin)
    await message.answer(t(lang, "checkin"))

@dp.message(Form.checkin)
async def input_checkin(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(checkin=message.text.strip())
    await state.set_state(Form.checkout)
    await message.answer(t(lang, "checkout"))

@dp.message(Form.checkout)
async def input_checkout(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(checkout=message.text.strip())
    await state.set_state(Form.budget)
    await message.answer(t(lang, "budget"), reply_markup=kb_skip(lang))

@dp.message(Form.budget)
async def input_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text.strip())
    await goto_transfer_or_phone(message, state)

@dp.callback_query(Form.budget, F.data == "skip")
async def skip_budget(cb: CallbackQuery, state: FSMContext):
    await state.update_data(budget="—")
    await cb.answer()
    await goto_transfer_or_phone(cb.message, state, uid=cb.from_user.id)


async def goto_transfer_or_phone(message, state, uid=None):
    """Mehmonxonadan keyin: agar 'both' bo'lsa transfer, aks holda telefon."""
    if uid is None:
        uid = message.from_user.id
    lang = UL(uid)
    data = await state.get_data()
    if data.get("service") == "both":
        await state.set_state(Form.tr_type)
        await message.answer(t(lang, "transfer_type"), reply_markup=kb_transfer_type(lang))
    else:
        await ask_phone(message, state, lang)


# ==================== TRANSFER OQIMI ====================
@dp.callback_query(Form.tr_type, F.data.startswith("trt:"))
async def choose_tr_type(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    await state.update_data(tr_type=cb.data.split(":")[1])
    await state.set_state(Form.tr_route)
    await cb.message.answer(t(lang, "transfer_route"))
    await cb.answer()

@dp.message(Form.tr_route)
async def input_tr_route(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(tr_route=message.text.strip())
    await state.set_state(Form.tr_date)
    await message.answer(t(lang, "transfer_date"))

@dp.message(Form.tr_date)
async def input_tr_date(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(tr_date=message.text.strip())
    await state.set_state(Form.tr_pax)
    await message.answer(t(lang, "pax"))

@dp.message(Form.tr_pax)
async def input_tr_pax(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    if not message.text.strip().isdigit():
        await message.answer(t(lang, "invalid_num"))
        return
    await state.update_data(tr_pax=message.text.strip())
    await ask_phone(message, state, lang)


# ==================== TELEFON + ISM ====================
async def ask_phone(message, state, lang):
    await state.set_state(Form.phone)
    await message.answer(t(lang, "phone"), reply_markup=kb_phone(lang))

@dp.message(Form.phone, F.contact)
async def phone_contact(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(Form.name)
    await message.answer(t(lang, "name"), reply_markup=ReplyKeyboardRemove())

@dp.message(Form.phone)
async def phone_text(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(phone=message.text.strip())
    await state.set_state(Form.name)
    await message.answer(t(lang, "name"), reply_markup=ReplyKeyboardRemove())

@dp.message(Form.name)
async def input_name(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(name=message.text.strip())
    data = await state.get_data()
    await state.clear()
    # so'rovni yuborish
    await send_to_admin(message, data, lang)
    await save_request(message, data, lang)
    await message.answer(t(lang, "done"), reply_markup=kb_menu(lang))


# ==================== ADMIN GURUHIGA YUBORISH ====================
def meal_label(lang, code):
    return {"ro": t(lang, "meal_ro"), "bb": t(lang, "meal_bb"),
            "hb": t(lang, "meal_hb"), "fb": t(lang, "meal_fb")}.get(code, code)

def trtype_label(lang, code):
    return {"airport": t(lang, "tr_airport"), "intercity": t(lang, "tr_intercity"),
            "ziyorat": t(lang, "tr_ziyorat")}.get(code, code)

def city_label(lang, code):
    return {"makkah": t(lang, "city_makkah"), "madinah": t(lang, "city_madinah"),
            "both": t(lang, "city_both")}.get(code, code)

def build_admin_text(user, data, lang):
    svc = data.get("service")
    type_str = {"hotel": t("uz","a_hotel"), "transfer": t("uz","a_transfer"),
                "both": f"{t('uz','a_hotel')} + {t('uz','a_transfer')}"}.get(svc, svc)
    lines = [f"{t('uz','a_new')}", f"{t('uz','a_type')}: {type_str}"]
    # mehmonxona qismi
    if svc in ("hotel", "both"):
        lines.append(f"{t('uz','a_city')}: {city_label('uz', data.get('city',''))}")
        stars = data.get("stars", "")
        lines.append(f"{t('uz','a_stars')}: {stars if stars=='any' else stars+'⭐'}")
        lines.append(f"{t('uz','a_meal')}: {meal_label('uz', data.get('meal',''))}")
        lines.append(f"{t('uz','a_guests')}: {data.get('guests','')}")
        lines.append(f"{t('uz','a_dates')}: {data.get('checkin','')} — {data.get('checkout','')}")
        lines.append(f"{t('uz','a_budget')}: {data.get('budget','—')}")
    # transfer qismi
    if svc in ("transfer", "both"):
        lines.append(f"{t('uz','a_trtype')}: {trtype_label('uz', data.get('tr_type',''))}")
        lines.append(f"{t('uz','a_route')}: {data.get('tr_route','')}")
        lines.append(f"{t('uz','a_dates')}: {data.get('tr_date','')}")
        lines.append(f"{t('uz','a_pax')}: {data.get('tr_pax','')}")
    # aloqa
    lines.append(f"{t('uz','a_name')}: {data.get('name','')}")
    lines.append(f"{t('uz','a_phone')}: {data.get('phone','')}")
    uname = f"@{user.username}" if user.username else user.full_name
    lines.append(f"{t('uz','a_lang')}: {lang.upper()} · {t('uz','a_user')}: {uname}")
    return "\n".join(lines)

async def send_to_admin(message, data, lang):
    if not ADMIN_GROUP_ID:
        logging.warning("ADMIN_GROUP_ID sozlanmagan!")
        return
    text = build_admin_text(message.from_user, data, lang)
    try:
        # parse_mode=None -> oddiy matn, maxsus belgilar (* _ [ ]) buzilmaydi
        await bot.send_message(ADMIN_GROUP_ID, text, parse_mode=None)
    except Exception as e:
        logging.error(f"Admin guruhga yuborishda xato: {e}")

async def save_request(message, data, lang):
    """So'rovlarni faylga saqlaymiz (tarix uchun)."""
    rec = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": message.from_user.username or message.from_user.full_name,
        "lang": lang, **data,
    }
    try:
        arr = []
        if os.path.exists(REQUESTS_FILE):
            with open(REQUESTS_FILE, "r", encoding="utf-8") as f:
                arr = json.load(f)
        arr.append(rec)
        with open(REQUESTS_FILE, "w", encoding="utf-8") as f:
            json.dump(arr, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Saqlashda xato: {e}")


# ==================== ISHGA TUSHIRISH ====================
async def main():
    logging.info("HIJAZ bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
