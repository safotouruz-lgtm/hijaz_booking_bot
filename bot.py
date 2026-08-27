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

# --- Aloqa ma'lumotlari (o'zingiznikini yozing) ---
CONTACT_PHONE = "+998911719900"              # qo'ng'iroq uchun (bo'shliqsiz)
CONTACT_TELEGRAM = "hijaz_booking"           # @siz  (@ belgisisiz)
CONTACT_WHATSAPP = "998911719900"            # WhatsApp raqami (+ va bo'shliqsiz)
CONTACT_INSTAGRAM = "hijaz_booking"          # instagram username (@ belgisisiz)

# --- Mashhur mehmonxonalar (Haram-ga yaqin). Xohlagancha tahrirlang ---
HOTELS = {
    "makkah": [
        "Fairmont Makkah Clock Royal Tower", "Raffles Makkah Palace",
        "Swissotel Al Maqam Makkah", "Pullman ZamZam Makkah",
        "Conrad Makkah", "Jabal Omar Hyatt Regency",
        "Address Jabal Omar Makkah", "Hilton Suites Makkah",
        "InterContinental Dar Al Tawhid", "Movenpick Hajar Tower Makkah",
        "Anjum Makkah Hotel", "DoubleTree by Hilton Jabal Omar",
        "Elaf Kinda Makkah", "Al Ghufran Safwah Tower",
    ],
    "madinah": [
        "Anwar Al Madinah Movenpick", "Pullman ZamZam Madinah",
        "The Oberoi Madinah", "Shaza Al Madinah",
        "Dar Al Iman InterContinental", "Hilton Madinah",
        "Madinah Marriott Hotel", "Dar Al Taqwa Hotel",
        "Taiba Front Hotel", "Dallah Taibah Hotel",
        "Crowne Plaza Madinah", "Saja Al Madinah Hotel",
        "Coral Al Madinah", "Al Muna Kareem Hotel",
    ],
}

# --- Transfer avtomobillari (sig'imi bilan). Xohlagancha tahrirlang ---
CARS = [
    "Camry",
    "GMC",
    "Hiace",
    "Staria",
    "Kia Carnival",
    "Avtobus 20",
    "Avtobus 50",
]

# --- Transfer yo'nalishlari. Xohlagancha tahrirlang ---
ROUTES = [
    "Jidda aeroport → Madina",
    "Madina ziyorat",
    "Madina → Makka",
    "Makka ziyorat",
    "Makka → Jidda aeroport",
    "Madina aeroport → Madina hotel",
]


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
    hotel = State()
    meal = State()
    guests = State()
    room_count = State()    # xonalar soni
    room_type = State()     # necha kishilik xona
    checkin = State()
    checkout = State()
    # ikkala shahar uchun alohida sanalar (both tanlanganda)
    mk_checkin = State()
    mk_checkout = State()
    md_checkin = State()
    md_checkout = State()
    budget = State()
    # transfer
    tr_type = State()
    tr_route_choose = State()
    tr_route = State()
    tr_date = State()
    tr_pax = State()
    tr_car = State()
    # umumiy
    phone = State()
    name = State()
    confirm = State()


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

def kb_hotel(lang, city):
    """Mehmonxona tanlash klaviaturasi (shahar bo'yicha + Farqi yo'q)."""
    rows = [[InlineKeyboardButton(text=t(lang, "hotel_any"), callback_data="hotel:any")]]
    # index bo'yicha ishlaymiz (nomlar uzun, callback_data cheklangan)
    if city == "both":
        names = HOTELS["makkah"] + HOTELS["madinah"]
    else:
        names = HOTELS.get(city, [])
    for i, name in enumerate(names):
        rows.append([InlineKeyboardButton(text=name, callback_data=f"hotel:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def hotel_name_by_index(city, idx):
    if city == "both":
        names = HOTELS["makkah"] + HOTELS["madinah"]
    else:
        names = HOTELS.get(city, [])
    if 0 <= idx < len(names):
        return names[idx]
    return ""

def kb_car(lang):
    """Avtomobil turi tanlash klaviaturasi (+ Farqi yo'q)."""
    rows = [[InlineKeyboardButton(text=t(lang, "car_any"), callback_data="car:any")]]
    for i, name in enumerate(CARS):
        rows.append([InlineKeyboardButton(text=f"🚗 {name}", callback_data=f"car:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def car_name_by_index(idx):
    if 0 <= idx < len(CARS):
        return CARS[idx]
    return ""

def kb_route(lang):
    """Yo'nalish tanlash klaviaturasi (+ Boshqa)."""
    rows = []
    for i, name in enumerate(ROUTES):
        rows.append([InlineKeyboardButton(text=f"📍 {name}", callback_data=f"route:{i}")])
    rows.append([InlineKeyboardButton(text=t(lang, "route_other"), callback_data="route:other")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def route_name_by_index(idx):
    if 0 <= idx < len(ROUTES):
        return ROUTES[idx]
    return ""

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

def kb_room_type(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "rt_single"), callback_data="rt:single"),
         InlineKeyboardButton(text=t(lang, "rt_double"), callback_data="rt:double")],
        [InlineKeyboardButton(text=t(lang, "rt_triple"), callback_data="rt:triple"),
         InlineKeyboardButton(text=t(lang, "rt_quad"), callback_data="rt:quad")],
        [InlineKeyboardButton(text=t(lang, "rt_mixed"), callback_data="rt:mixed")],
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
@dp.message(Command("bekor", "cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    cur = await state.get_state()
    await state.clear()
    if cur is not None:
        await message.answer(t(lang, "cancelled"), reply_markup=kb_menu(lang))
    else:
        await message.answer(t(lang, "welcome"), reply_markup=kb_menu(lang))

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
    # Telefon matnda (tel: URL Telegram inline tugmada ishlamaydi)
    text = t(lang, "contact_txt") + f"\n\n📞 {CONTACT_PHONE}"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_tg"), url=f"https://t.me/{CONTACT_TELEGRAM}"),
         InlineKeyboardButton(text=t(lang, "btn_wa"), url=f"https://wa.me/{CONTACT_WHATSAPP}")],
        [InlineKeyboardButton(text=t(lang, "btn_ig"), url=f"https://instagram.com/{CONTACT_INSTAGRAM}")],
    ])
    await cb.message.answer(text, reply_markup=kb, parse_mode=None)
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
        await state.set_state(Form.tr_route_choose)
        await cb.message.answer(t(lang, "transfer_route"), reply_markup=kb_route(lang))
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
    data = await state.get_data()
    city = data.get("city", "")
    # aniq mehmonxona so'raymiz (ixtiyoriy)
    await state.set_state(Form.hotel)
    await cb.message.answer(t(lang, "hotel_q"), reply_markup=kb_hotel(lang, city))
    await cb.answer()

@dp.callback_query(Form.hotel, F.data.startswith("hotel:"))
async def choose_hotel(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    val = cb.data.split(":")[1]
    data = await state.get_data()
    if val == "any":
        await state.update_data(hotel="")
    else:
        name = hotel_name_by_index(data.get("city", ""), int(val))
        await state.update_data(hotel=name)
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
    await state.set_state(Form.room_count)
    await message.answer(t(lang, "room_count"))

@dp.message(Form.room_count)
async def input_room_count(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    if not message.text.strip().isdigit():
        await message.answer(t(lang, "invalid_num"))
        return
    await state.update_data(room_count=message.text.strip())
    await state.set_state(Form.room_type)
    await message.answer(t(lang, "room_type"), reply_markup=kb_room_type(lang))

@dp.callback_query(Form.room_type, F.data.startswith("rt:"))
async def choose_room_type(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    await state.update_data(room_type=cb.data.split(":")[1])
    data = await state.get_data()
    await cb.answer()
    if data.get("city") == "both":
        # ikkala shahar - alohida sanalar, Makkadan boshlaymiz
        await state.set_state(Form.mk_checkin)
        await cb.message.answer(t(lang, "mk_checkin"))
    else:
        await state.set_state(Form.checkin)
        await cb.message.answer(t(lang, "checkin"))

# --- Bitta shahar: oddiy sanalar ---
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

# --- Ikkala shahar: Makka sanalari, keyin Madina sanalari ---
@dp.message(Form.mk_checkin)
async def input_mk_checkin(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(mk_checkin=message.text.strip())
    await state.set_state(Form.mk_checkout)
    await message.answer(t(lang, "mk_checkout"))

@dp.message(Form.mk_checkout)
async def input_mk_checkout(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(mk_checkout=message.text.strip())
    await state.set_state(Form.md_checkin)
    await message.answer(t(lang, "md_checkin"))

@dp.message(Form.md_checkin)
async def input_md_checkin(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(md_checkin=message.text.strip())
    await state.set_state(Form.md_checkout)
    await message.answer(t(lang, "md_checkout"))

@dp.message(Form.md_checkout)
async def input_md_checkout(message: Message, state: FSMContext):
    lang = UL(message.from_user.id)
    await state.update_data(md_checkout=message.text.strip())
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
        await state.set_state(Form.tr_route_choose)
        await message.answer(t(lang, "transfer_route"), reply_markup=kb_route(lang))
    else:
        await ask_phone(message, state, lang)


# ==================== TRANSFER OQIMI ====================
@dp.callback_query(Form.tr_route_choose, F.data.startswith("route:"))
async def choose_route(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    val = cb.data.split(":")[1]
    if val == "other":
        # o'zi yozadi
        await state.set_state(Form.tr_route)
        await cb.message.answer(t(lang, "transfer_route_manual"))
    else:
        await state.update_data(tr_route=route_name_by_index(int(val)))
        await state.set_state(Form.tr_date)
        await cb.message.answer(t(lang, "transfer_date"))
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
    # mashina turini so'raymiz (ixtiyoriy)
    await state.set_state(Form.tr_car)
    await message.answer(t(lang, "car_q"), reply_markup=kb_car(lang))

@dp.callback_query(Form.tr_car, F.data.startswith("car:"))
async def choose_car(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    val = cb.data.split(":")[1]
    if val == "any":
        await state.update_data(tr_car="")
    else:
        await state.update_data(tr_car=car_name_by_index(int(val)))
    await ask_phone(cb.message, state, lang, uid=cb.from_user.id)
    await cb.answer()


# ==================== TELEFON + ISM ====================
async def ask_phone(message, state, lang, uid=None):
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
    # tasdiqlash ekranini ko'rsatamiz (yubormasdan oldin)
    await state.set_state(Form.confirm)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "btn_confirm"), callback_data="confirm_send")],
        [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="confirm_cancel")],
    ])
    await message.answer(build_customer_summary(data, lang), reply_markup=kb, parse_mode=None)

@dp.callback_query(Form.confirm, F.data == "confirm_send")
async def confirm_send(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    data = await state.get_data()
    await state.clear()
    # so'rov raqamini olamiz (admin va mijozga bir xil raqam)
    req_no = get_next_request_no()
    await send_to_admin(cb.message, data, lang, user=cb.from_user, req_no=req_no)
    await save_request_user(cb.from_user, data, lang)
    # mijozga javob + so'rov raqami
    done_text = t(lang, "done") + f"\n\n🎫 {t(lang, 'req_no')}: #{req_no:03d}"
    await cb.message.answer(done_text, reply_markup=kb_menu(lang), parse_mode=None)
    await cb.answer()

@dp.callback_query(Form.confirm, F.data == "confirm_cancel")
async def confirm_cancel(cb: CallbackQuery, state: FSMContext):
    lang = UL(cb.from_user.id)
    await state.clear()
    await cb.message.answer(t(lang, "cancelled"), reply_markup=kb_menu(lang))
    await cb.answer()


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

def build_customer_summary(data, lang):
    """Mijoz uchun so'rov xulosasi (uning tilida, tasdiqlash uchun)."""
    svc = data.get("service")
    type_str = {"hotel": t(lang,"c_hotel"), "transfer": t(lang,"c_transfer"),
                "both": f"{t(lang,'c_hotel')} + {t(lang,'c_transfer')}"}.get(svc, svc)
    lines = [t(lang,"confirm_title"), "", f"{t(lang,'c_service')}: {type_str}"]
    if svc in ("hotel", "both"):
        lines.append(f"{t(lang,'a_city')}: {city_label(lang, data.get('city',''))}")
        stars = data.get("stars", "")
        lines.append(f"{t(lang,'a_stars')}: {stars if stars=='any' else stars+'⭐'}")
        if data.get("hotel"):
            lines.append(f"{t(lang,'a_hotel_sel')}: {data.get('hotel')}")
        lines.append(f"{t(lang,'a_meal')}: {meal_label(lang, data.get('meal',''))}")
        lines.append(f"{t(lang,'a_guests')}: {data.get('guests','')}")
        lines.append(f"{t(lang,'a_rooms')}: {data.get('room_count','')}")
        rt = data.get('room_type', '')
        rt_names = {'single': t(lang,'rt_single'), 'double': t(lang,'rt_double'),
                    'triple': t(lang,'rt_triple'), 'quad': t(lang,'rt_quad'),
                    'mixed': t(lang,'rt_mixed')}
        lines.append(f"{t(lang,'a_roomtype')}: {rt_names.get(rt, rt)}")
        if data.get("city") == "both":
            lines.append(f"{t(lang,'a_mk_dates')}: {data.get('mk_checkin','')} — {data.get('mk_checkout','')}")
            lines.append(f"{t(lang,'a_md_dates')}: {data.get('md_checkin','')} — {data.get('md_checkout','')}")
        else:
            lines.append(f"{t(lang,'a_dates')}: {data.get('checkin','')} — {data.get('checkout','')}")
        lines.append(f"{t(lang,'a_budget')}: {data.get('budget','—')}")
    if svc in ("transfer", "both"):
        lines.append(f"{t(lang,'a_route')}: {data.get('tr_route','')}")
        lines.append(f"{t(lang,'a_dates')}: {data.get('tr_date','')}")
        lines.append(f"{t(lang,'a_pax')}: {data.get('tr_pax','')}")
        if data.get('tr_car'):
            lines.append(f"{t(lang,'a_car')}: {data.get('tr_car')}")
    lines.append(f"{t(lang,'a_name')}: {data.get('name','')}")
    lines.append(f"{t(lang,'a_phone')}: {data.get('phone','')}")
    lines.append("")
    lines.append(t(lang,"confirm_ask"))
    return "\n".join(lines)


def build_admin_text(user, data, lang, req_no=None):
    svc = data.get("service")
    type_str = {"hotel": t("uz","a_hotel"), "transfer": t("uz","a_transfer"),
                "both": f"{t('uz','a_hotel')} + {t('uz','a_transfer')}"}.get(svc, svc)
    # sarlavha: yangi so'rov + raqam + vaqt
    header = t('uz','a_new')
    if req_no:
        header = f"{t('uz','a_new')}  #{req_no:03d}"
    now = datetime.now().strftime("%d.%m.%Y  %H:%M")
    lines = [header, f"🕐 {now}", "", f"{t('uz','a_type')}: {type_str}"]
    # mehmonxona qismi
    if svc in ("hotel", "both"):
        lines.append(f"{t('uz','a_city')}: {city_label('uz', data.get('city',''))}")
        stars = data.get("stars", "")
        lines.append(f"{t('uz','a_stars')}: {stars if stars=='any' else stars+'⭐'}")
        if data.get("hotel"):
            lines.append(f"{t('uz','a_hotel_sel')}: {data.get('hotel')}")
        lines.append(f"{t('uz','a_meal')}: {meal_label('uz', data.get('meal',''))}")
        lines.append(f"{t('uz','a_guests')}: {data.get('guests','')}")
        lines.append(f"{t('uz','a_rooms')}: {data.get('room_count','')}")
        rt = data.get('room_type', '')
        rt_names = {'single': t('uz','rt_single'), 'double': t('uz','rt_double'),
                    'triple': t('uz','rt_triple'), 'quad': t('uz','rt_quad'),
                    'mixed': t('uz','rt_mixed')}
        lines.append(f"{t('uz','a_roomtype')}: {rt_names.get(rt, rt)}")
        if data.get("city") == "both":
            lines.append(f"{t('uz','a_mk_dates')}: {data.get('mk_checkin','')} — {data.get('mk_checkout','')}")
            lines.append(f"{t('uz','a_md_dates')}: {data.get('md_checkin','')} — {data.get('md_checkout','')}")
        else:
            lines.append(f"{t('uz','a_dates')}: {data.get('checkin','')} — {data.get('checkout','')}")
        lines.append(f"{t('uz','a_budget')}: {data.get('budget','—')}")
    # transfer qismi
    if svc in ("transfer", "both"):
        lines.append(f"{t('uz','a_route')}: {data.get('tr_route','')}")
        lines.append(f"{t('uz','a_dates')}: {data.get('tr_date','')}")
        lines.append(f"{t('uz','a_pax')}: {data.get('tr_pax','')}")
        if data.get('tr_car'):
            lines.append(f"{t('uz','a_car')}: {data.get('tr_car')}")
    # aloqa
    lines.append(f"{t('uz','a_name')}: {data.get('name','')}")
    lines.append(f"{t('uz','a_phone')}: {data.get('phone','')}")
    uname = f"@{user.username}" if user.username else user.full_name
    lines.append(f"{t('uz','a_lang')}: {lang.upper()} · {t('uz','a_user')}: {uname}")
    return "\n".join(lines)

async def send_to_admin(message, data, lang, user=None, req_no=None):
    if not ADMIN_GROUP_ID:
        logging.warning("ADMIN_GROUP_ID sozlanmagan!")
        return
    if user is None:
        user = message.from_user
    text = build_admin_text(user, data, lang, req_no=req_no)
    try:
        # parse_mode=None -> oddiy matn, maxsus belgilar (* _ [ ]) buzilmaydi
        await bot.send_message(ADMIN_GROUP_ID, text, parse_mode=None)
    except Exception as e:
        logging.error(f"Admin guruhga yuborishda xato: {e}")

def get_next_request_no():
    """Keyingi so'rov raqamini qaytaradi (mavjud so'rovlar soni + 1)."""
    try:
        if os.path.exists(REQUESTS_FILE):
            with open(REQUESTS_FILE, "r", encoding="utf-8") as f:
                arr = json.load(f)
            return len(arr) + 1
    except Exception:
        pass
    return 1

async def save_request_user(user, data, lang):
    """So'rovni faylga saqlaymiz (user obyekti bilan)."""
    rec = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": user.username or user.full_name,
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
