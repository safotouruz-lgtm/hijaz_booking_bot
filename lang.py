# -*- coding: utf-8 -*-
"""HIJAZ bot — 5 tilli tarjimalar: O'zbek, Rus, Ingliz, Arab, Turk"""

TR = {
    # ==================== O'ZBEK ====================
    "uz": {
        "lang_name": "🇺🇿 O'zbek",
        "welcome": (
            "🕋 *HIJAZ — Saudiya mehmonxona broni*\n\n"
            "Assalomu alaykum! Makka va Madinada mehmonxona bron qilish "
            "hamda transfer xizmati uchun so'rov qoldiring.\n\n"
            "Quyidagidan tanlang 👇"
        ),
        "menu_booking": "🏨 Bron so'rovi",
        "menu_contact": "📞 Bog'lanish",
        "menu_info": "ℹ️ Ma'lumot",
        "menu_lang": "🌐 Tilni o'zgartirish",
        "choose_service": "Sizga nima kerak?",
        "svc_hotel": "🏨 Mehmonxona",
        "svc_transfer": "🚗 Transfer",
        "svc_both": "🏨+🚗 Ikkalasi",
        "choose_city": "Qaysi shahar?",
        "city_makkah": "🕋 Makka",
        "city_madinah": "🕌 Madina",
        "city_both": "Ikkalasi",
        "hotel_stars": "Mehmonxona darajasi?",
        "stars_any": "Farqi yo'q",
        "meal": "Taomlanish turi?",
        "meal_ro": "Faqat yashash",
        "meal_bb": "Nonushta bilan",
        "meal_hb": "Yarim pansion",
        "meal_fb": "To'liq pansion",
        "guests": "Necha kishi? (raqam kiriting)",
        "checkin": "Kirish sanasi? (masalan: 15/08/2026)",
        "checkout": "Chiqish sanasi? (masalan: 18/08/2026)",
        "budget": "Budjet (bir kecha uchun, $)? Bilmasangiz 'O'tkazish' bosing",
        "skip": "O'tkazish",
        "transfer_type": "Transfer turi?",
        "tr_airport": "✈️ Aeroport ↔ mehmonxona",
        "tr_intercity": "🚙 Shaharlararo (Makka ↔ Madina)",
        "tr_ziyorat": "🕌 Ziyorat / ekskursiya",
        "transfer_route": "Yo'nalishni yozing (masalan: Jidda aeroport → Makka)",
        "transfer_date": "Transfer sanasi? (masalan: 15/08/2026)",
        "pax": "Necha yo'lovchi? (raqam)",
        "phone": "📱 Telefon raqamingiz? (tugmani bosing yoki yozing)",
        "phone_btn": "📱 Raqamni yuborish",
        "name": "Ismingiz?",
        "done": (
            "✅ *So'rovingiz qabul qilindi!*\n\n"
            "HIJAZ jamoasi tez orada siz bilan bog'lanadi, ichaAlloh.\n"
            "E'tiboringiz uchun rahmat! 🕋"
        ),
        "contact_txt": "📞 *HIJAZ bilan bog'lanish:*\n\nTelefon: +998 91 171 99 00\nTelegram: @hijaz_booking",
        "info_txt": (
            "ℹ️ *HIJAZ haqida*\n\n"
            "HIJAZ — Makka va Madinada ishonchli mehmonxona broni va transfer xizmati.\n\n"
            "• Haramga yaqin mehmonxonalar\n• Aeroport va shaharlararo transfer\n"
            "• Ziyorat uyushtirish\n• Qulay narxlar\n\n"
            "Bron uchun 🏨 tugmasini bosing."
        ),
        "choose_lang": "Tilni tanlang / Выберите язык / Choose language:",
        "invalid_num": "Iltimos, raqam kiriting.",
        "back": "⬅️ Orqaga",
        # admin so'rov teglari
        "a_new": "🔔 YANGI SO'ROV",
        "a_type": "Turi",
        "a_hotel": "Mehmonxona",
        "a_transfer": "Transfer",
        "a_city": "Shahar",
        "a_stars": "Daraja",
        "a_meal": "Taomlanish",
        "a_guests": "Mehmonlar",
        "a_dates": "Sana",
        "a_budget": "Budjet",
        "a_trtype": "Transfer turi",
        "a_route": "Yo'nalish",
        "a_pax": "Yo'lovchilar",
        "a_phone": "Telefon",
        "a_name": "Ism",
        "a_lang": "Til",
        "a_user": "Foydalanuvchi",
        "nights": "kecha",
    },
    # ==================== РУССКИЙ ====================
    "ru": {
        "lang_name": "🇷🇺 Русский",
        "welcome": (
            "🕋 *HIJAZ — Бронирование отелей в Саудовской Аравии*\n\n"
            "Ассаляму алейкум! Оставьте заявку на бронирование отеля в Мекке "
            "и Медине, а также на трансфер.\n\n"
            "Выберите ниже 👇"
        ),
        "menu_booking": "🏨 Оставить заявку",
        "menu_contact": "📞 Контакты",
        "menu_info": "ℹ️ Информация",
        "menu_lang": "🌐 Сменить язык",
        "choose_service": "Что вам нужно?",
        "svc_hotel": "🏨 Отель",
        "svc_transfer": "🚗 Трансфер",
        "svc_both": "🏨+🚗 Оба",
        "choose_city": "Какой город?",
        "city_makkah": "🕋 Мекка",
        "city_madinah": "🕌 Медина",
        "city_both": "Оба",
        "hotel_stars": "Категория отеля?",
        "stars_any": "Не важно",
        "meal": "Тип питания?",
        "meal_ro": "Только проживание",
        "meal_bb": "Завтрак",
        "meal_hb": "Полупансион",
        "meal_fb": "Полный пансион",
        "guests": "Сколько человек? (введите число)",
        "checkin": "Дата заезда? (например: 15/08/2026)",
        "checkout": "Дата выезда? (например: 18/08/2026)",
        "budget": "Бюджет (за ночь, $)? Если не знаете — нажмите 'Пропустить'",
        "skip": "Пропустить",
        "transfer_type": "Тип трансфера?",
        "tr_airport": "✈️ Аэропорт ↔ отель",
        "tr_intercity": "🚙 Между городами (Мекка ↔ Медина)",
        "tr_ziyorat": "🕌 Зиярат / экскурсия",
        "transfer_route": "Напишите маршрут (например: аэропорт Джидда → Мекка)",
        "transfer_date": "Дата трансфера? (например: 15/08/2026)",
        "pax": "Сколько пассажиров? (число)",
        "phone": "📱 Ваш номер телефона? (нажмите кнопку или напишите)",
        "phone_btn": "📱 Отправить номер",
        "name": "Ваше имя?",
        "done": (
            "✅ *Ваша заявка принята!*\n\n"
            "Команда HIJAZ скоро свяжется с вами, инша Аллах.\n"
            "Спасибо за обращение! 🕋"
        ),
        "contact_txt": "📞 *Связь с HIJAZ:*\n\nТелефон: +998 91 171 99 00\nTelegram: @hijaz_booking",
        "info_txt": (
            "ℹ️ *О HIJAZ*\n\n"
            "HIJAZ — надёжное бронирование отелей и трансфер в Мекке и Медине.\n\n"
            "• Отели рядом с Харамом\n• Аэропорт и междугородний трансфер\n"
            "• Организация зиярата\n• Удобные цены\n\n"
            "Для заявки нажмите 🏨."
        ),
        "choose_lang": "Tilni tanlang / Выберите язык / Choose language:",
        "invalid_num": "Пожалуйста, введите число.",
        "back": "⬅️ Назад",
        "a_new": "🔔 НОВАЯ ЗАЯВКА",
        "a_type": "Тип",
        "a_hotel": "Отель",
        "a_transfer": "Трансфер",
        "a_city": "Город",
        "a_stars": "Категория",
        "a_meal": "Питание",
        "a_guests": "Гости",
        "a_dates": "Даты",
        "a_budget": "Бюджет",
        "a_trtype": "Тип трансфера",
        "a_route": "Маршрут",
        "a_pax": "Пассажиры",
        "a_phone": "Телефон",
        "a_name": "Имя",
        "a_lang": "Язык",
        "a_user": "Пользователь",
        "nights": "ночей",
    },
    # ==================== ENGLISH ====================
    "en": {
        "lang_name": "🇬🇧 English",
        "welcome": (
            "🕋 *HIJAZ — Saudi Hotel Booking*\n\n"
            "Assalamu alaikum! Send a request to book a hotel in Makkah "
            "and Madinah, and for transfer service.\n\n"
            "Please choose below 👇"
        ),
        "menu_booking": "🏨 Booking Request",
        "menu_contact": "📞 Contact",
        "menu_info": "ℹ️ Info",
        "menu_lang": "🌐 Change language",
        "choose_service": "What do you need?",
        "svc_hotel": "🏨 Hotel",
        "svc_transfer": "🚗 Transfer",
        "svc_both": "🏨+🚗 Both",
        "choose_city": "Which city?",
        "city_makkah": "🕋 Makkah",
        "city_madinah": "🕌 Madinah",
        "city_both": "Both",
        "hotel_stars": "Hotel category?",
        "stars_any": "Any",
        "meal": "Meal plan?",
        "meal_ro": "Room only",
        "meal_bb": "Bed & Breakfast",
        "meal_hb": "Half board",
        "meal_fb": "Full board",
        "guests": "How many guests? (enter a number)",
        "checkin": "Check-in date? (e.g. 15/08/2026)",
        "checkout": "Check-out date? (e.g. 18/08/2026)",
        "budget": "Budget (per night, $)? If unknown, press 'Skip'",
        "skip": "Skip",
        "transfer_type": "Transfer type?",
        "tr_airport": "✈️ Airport ↔ hotel",
        "tr_intercity": "🚙 Intercity (Makkah ↔ Madinah)",
        "tr_ziyorat": "🕌 Ziyarat / excursion",
        "transfer_route": "Write the route (e.g. Jeddah airport → Makkah)",
        "transfer_date": "Transfer date? (e.g. 15/08/2026)",
        "pax": "How many passengers? (number)",
        "phone": "📱 Your phone number? (press button or type)",
        "phone_btn": "📱 Send number",
        "name": "Your name?",
        "done": (
            "✅ *Your request has been received!*\n\n"
            "The HIJAZ team will contact you soon, in sha Allah.\n"
            "Thank you! 🕋"
        ),
        "contact_txt": "📞 *Contact HIJAZ:*\n\nPhone: +998 91 171 99 00\nTelegram: @hijaz_booking",
        "info_txt": (
            "ℹ️ *About HIJAZ*\n\n"
            "HIJAZ — reliable hotel booking and transfer in Makkah and Madinah.\n\n"
            "• Hotels near the Haram\n• Airport & intercity transfer\n"
            "• Ziyarat arrangement\n• Convenient prices\n\n"
            "Press 🏨 to make a request."
        ),
        "choose_lang": "Tilni tanlang / Выберите язык / Choose language:",
        "invalid_num": "Please enter a number.",
        "back": "⬅️ Back",
        "a_new": "🔔 NEW REQUEST",
        "a_type": "Type",
        "a_hotel": "Hotel",
        "a_transfer": "Transfer",
        "a_city": "City",
        "a_stars": "Category",
        "a_meal": "Meal",
        "a_guests": "Guests",
        "a_dates": "Dates",
        "a_budget": "Budget",
        "a_trtype": "Transfer type",
        "a_route": "Route",
        "a_pax": "Passengers",
        "a_phone": "Phone",
        "a_name": "Name",
        "a_lang": "Language",
        "a_user": "User",
        "nights": "nights",
    },
    # ==================== العربية ====================
    "ar": {
        "lang_name": "🇸🇦 العربية",
        "welcome": (
            "🕋 *حجاز — حجز الفنادق في السعودية*\n\n"
            "السلام عليكم! أرسل طلباً لحجز فندق في مكة والمدينة، وكذلك خدمة النقل.\n\n"
            "اختر من الأسفل 👇"
        ),
        "menu_booking": "🏨 طلب حجز",
        "menu_contact": "📞 تواصل",
        "menu_info": "ℹ️ معلومات",
        "menu_lang": "🌐 تغيير اللغة",
        "choose_service": "ماذا تحتاج؟",
        "svc_hotel": "🏨 فندق",
        "svc_transfer": "🚗 نقل",
        "svc_both": "🏨+🚗 كلاهما",
        "choose_city": "أي مدينة؟",
        "city_makkah": "🕋 مكة",
        "city_madinah": "🕌 المدينة",
        "city_both": "كلاهما",
        "hotel_stars": "فئة الفندق؟",
        "stars_any": "لا يهم",
        "meal": "نوع الوجبات؟",
        "meal_ro": "الإقامة فقط",
        "meal_bb": "مع الإفطار",
        "meal_hb": "نصف إقامة",
        "meal_fb": "إقامة كاملة",
        "guests": "كم عدد النزلاء؟ (أدخل رقماً)",
        "checkin": "تاريخ الوصول؟ (مثال: 15/08/2026)",
        "checkout": "تاريخ المغادرة؟ (مثال: 18/08/2026)",
        "budget": "الميزانية (لليلة، $)؟ إن لم تعرف اضغط 'تخطي'",
        "skip": "تخطي",
        "transfer_type": "نوع النقل؟",
        "tr_airport": "✈️ المطار ↔ الفندق",
        "tr_intercity": "🚙 بين المدن (مكة ↔ المدينة)",
        "tr_ziyorat": "🕌 زيارة / رحلة",
        "transfer_route": "اكتب المسار (مثال: مطار جدة → مكة)",
        "transfer_date": "تاريخ النقل؟ (مثال: 15/08/2026)",
        "pax": "كم عدد الركاب؟ (رقم)",
        "phone": "📱 رقم هاتفك؟ (اضغط الزر أو اكتب)",
        "phone_btn": "📱 إرسال الرقم",
        "name": "اسمك؟",
        "done": (
            "✅ *تم استلام طلبك!*\n\n"
            "سيتواصل معك فريق حجاز قريباً إن شاء الله.\n"
            "شكراً لك! 🕋"
        ),
        "contact_txt": "📞 *تواصل مع حجاز:*\n\nالهاتف: +998 91 171 99 00\nتيليجرام: @hijaz_booking",
        "info_txt": (
            "ℹ️ *عن حجاز*\n\n"
            "حجاز — حجز فنادق موثوق وخدمة نقل في مكة والمدينة.\n\n"
            "• فنادق قرب الحرم\n• نقل من المطار وبين المدن\n"
            "• تنظيم الزيارات\n• أسعار مناسبة\n\n"
            "اضغط 🏨 لتقديم طلب."
        ),
        "choose_lang": "Tilni tanlang / Выберите язык / Choose language:",
        "invalid_num": "الرجاء إدخال رقم.",
        "back": "⬅️ رجوع",
        "a_new": "🔔 طلب جديد",
        "a_type": "النوع",
        "a_hotel": "فندق",
        "a_transfer": "نقل",
        "a_city": "المدينة",
        "a_stars": "الفئة",
        "a_meal": "الوجبات",
        "a_guests": "النزلاء",
        "a_dates": "التواريخ",
        "a_budget": "الميزانية",
        "a_trtype": "نوع النقل",
        "a_route": "المسار",
        "a_pax": "الركاب",
        "a_phone": "الهاتف",
        "a_name": "الاسم",
        "a_lang": "اللغة",
        "a_user": "المستخدم",
        "nights": "ليالٍ",
    },
    # ==================== TÜRKÇE ====================
    "tr": {
        "lang_name": "🇹🇷 Türkçe",
        "welcome": (
            "🕋 *HIJAZ — Suudi Arabistan Otel Rezervasyonu*\n\n"
            "Esselamu aleykum! Mekke ve Medine'de otel rezervasyonu ve "
            "transfer hizmeti için talep bırakın.\n\n"
            "Aşağıdan seçin 👇"
        ),
        "menu_booking": "🏨 Rezervasyon talebi",
        "menu_contact": "📞 İletişim",
        "menu_info": "ℹ️ Bilgi",
        "menu_lang": "🌐 Dili değiştir",
        "choose_service": "Neye ihtiyacınız var?",
        "svc_hotel": "🏨 Otel",
        "svc_transfer": "🚗 Transfer",
        "svc_both": "🏨+🚗 İkisi",
        "choose_city": "Hangi şehir?",
        "city_makkah": "🕋 Mekke",
        "city_madinah": "🕌 Medine",
        "city_both": "İkisi",
        "hotel_stars": "Otel kategorisi?",
        "stars_any": "Farketmez",
        "meal": "Yemek tipi?",
        "meal_ro": "Sadece konaklama",
        "meal_bb": "Kahvaltı dahil",
        "meal_hb": "Yarım pansiyon",
        "meal_fb": "Tam pansiyon",
        "guests": "Kaç kişi? (sayı girin)",
        "checkin": "Giriş tarihi? (örn: 15/08/2026)",
        "checkout": "Çıkış tarihi? (örn: 18/08/2026)",
        "budget": "Bütçe (gecelik, $)? Bilmiyorsanız 'Atla' basın",
        "skip": "Atla",
        "transfer_type": "Transfer tipi?",
        "tr_airport": "✈️ Havalimanı ↔ otel",
        "tr_intercity": "🚙 Şehirlerarası (Mekke ↔ Medine)",
        "tr_ziyorat": "🕌 Ziyaret / gezi",
        "transfer_route": "Güzergahı yazın (örn: Cidde havalimanı → Mekke)",
        "transfer_date": "Transfer tarihi? (örn: 15/08/2026)",
        "pax": "Kaç yolcu? (sayı)",
        "phone": "📱 Telefon numaranız? (butona basın veya yazın)",
        "phone_btn": "📱 Numarayı gönder",
        "name": "Adınız?",
        "done": (
            "✅ *Talebiniz alındı!*\n\n"
            "HIJAZ ekibi en kısa sürede sizinle iletişime geçecek, inşallah.\n"
            "Teşekkürler! 🕋"
        ),
        "contact_txt": "📞 *HIJAZ ile iletişim:*\n\nTelefon: +998 91 171 99 00\nTelegram: @hijaz_booking",
        "info_txt": (
            "ℹ️ *HIJAZ Hakkında*\n\n"
            "HIJAZ — Mekke ve Medine'de güvenilir otel rezervasyonu ve transfer.\n\n"
            "• Harem'e yakın oteller\n• Havalimanı ve şehirlerarası transfer\n"
            "• Ziyaret organizasyonu\n• Uygun fiyatlar\n\n"
            "Talep için 🏨 basın."
        ),
        "choose_lang": "Tilni tanlang / Выберите язык / Choose language:",
        "invalid_num": "Lütfen bir sayı girin.",
        "back": "⬅️ Geri",
        "a_new": "🔔 YENİ TALEP",
        "a_type": "Tür",
        "a_hotel": "Otel",
        "a_transfer": "Transfer",
        "a_city": "Şehir",
        "a_stars": "Kategori",
        "a_meal": "Yemek",
        "a_guests": "Misafirler",
        "a_dates": "Tarihler",
        "a_budget": "Bütçe",
        "a_trtype": "Transfer tipi",
        "a_route": "Güzergah",
        "a_pax": "Yolcular",
        "a_phone": "Telefon",
        "a_name": "İsim",
        "a_lang": "Dil",
        "a_user": "Kullanıcı",
        "nights": "gece",
    },
}


def t(lang, key):
    """Tarjima olish. Til topilmasa o'zbekcha qaytaradi."""
    return TR.get(lang, TR["uz"]).get(key, TR["uz"].get(key, key))
