import os
import logging
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, 
    filters, ContextTypes, ConversationHandler
)
import database as db
import mailer

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

# Logging sozlash
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Token va Bazani ishga tushirish
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
    raise RuntimeError(
        "Missing Telegram bot token. Set TELEGRAM_TOKEN as an environment variable or add it to a .env file."
    )

db.init_db()

# Conversation States (Holatlar)
LANG, REG_NAME, REG_PHONE, REG_LOCATION, REG_EMAIL, MAIN_MENU, SECTION_VIEW, Q_VIEW, PROBLEM_STATE, SETTINGS_STATE, ABOUT_STATE = range(11)

# Matnlar lokalizatsiyasi
STRINGS = {
    'uz': {
        'welcome': "Xush kelibsiz! Iltimos, tilni tanlang:",
        'ask_name': "Ro'yxatdan o'tishni boshlaymiz. Ism va familiyangizni kiriting:",
        'ask_phone': "Telefon raqamingizni yuboring (Tugmani bosing yoki kiriting):",
        'ask_loc': "Yashash manzilingizni yoki lokatsiyangizni yuboring:",
        'reg_success': "Siz muvaffaqiyatli ro'yxatdan o'tdingiz! 🎉",
        'main_menu': "Asosiy Menyudasiz. Bo'limlardan birini tanlang:",
        'btn_phone': "📱 Telefon raqamni yuborish",
        'btn_sections': "📚 Bilimlar Bo'limi (IELTS/SAT)",
        'btn_problem': "⚠️ Muammo va Takliflar",
        'btn_resources': "🌐 Resurslar",
        'btn_web': "🌍 Web App",
        'btn_settings': "⚙️ Sozlamalar",
        'btn_about': "ℹ️ Bot haqida",
        'btn_logout': "🚪 Logout",
        'select_section': "Qaysi yo'nalish bo'yicha savollarga javob olishni xohlaysiz?",
        'select_question': "Savollardan birini tanlang:",
        'problem_prompt': "Botga nima qo'shilishini istaysiz? Shikoyatingiz yoki taklifingiz bormi? Batafsil yozib qoldiring:",
        'problem_received': "Rahmat! Sizning murojaatingiz E-mail orqali yuborildi. 📬\nAgar sizga ham xabar kerak bo'lsa, u sizning ro'yxatdan o'tgan email manzilingizga yuboriladi.\nQo'shimcha yordam kerak bo'lsa, quyidagi admin bilan bog'laning:\nTel: 99 702 1775\nEmail: aslonovdiyorbek333@gmail.com",
        'about_text': "Ushbu bot talabalarga IELTS, SAT va universitet ma'lumotlari bo'yicha yordam beradi. Har qanday savolga javob berish uchun menudan kerakli bo'limni tanlang.\n\nBot to'liq lokal bazaga asoslangan va API kalitlari talab qilinmaydi.",
        'ask_email': "Iltimos, o'z elektron pochta manzilingizni yuboring:",
        'question_not_found': "Kechirasiz, bu savol topilmadi. Iltimos menyudan savol tanlang yoki boshqa so'z bilan so'rang.",
        'btn_back': "⬅️ Orqaga",
        'settings_txt': "Sozlamalar bo'limi. Tilni o'zgartirishingiz mumkin:"
    },
    'en': {
        'welcome': "Welcome! Please select your language:",
        'ask_name': "Let's start registration. Enter your full name:",
        'ask_phone': "Send your phone number (Press the button or type):",
        'ask_loc': "Send your current location or address:",
        'reg_success': "You have successfully registered! 🎉",
        'main_menu': "Main Menu. Choose one of the sections:",
        'btn_phone': "📱 Send Phone Number",
        'btn_sections': "📚 Study Sections (IELTS/SAT)",
        'btn_resources': "🌐 Resources",
        'btn_web': "🌍 Web App",
        'btn_problem': "⚠️ Issues & Suggestions",
        'btn_settings': "⚙️ Settings",
        'btn_about': "ℹ️ About Bot",
        'btn_logout': "🚪 Logout",
        'select_section': "Which direction would you like to get answers for?",
        'select_question': "Choose one of the questions:",
        'problem_prompt': "What features would you like to see? Do you have complaints? Please write here in detail:",
        'problem_received': "Thank you! Your report has been submitted to the admin via email. 📬\nA copy will also be sent to your registered email address if available.\nIf you need more help, contact our admin:\nTel: 99 702 1775\nEmail: aslonovdiyorbek333@gmail.com",
        'resources_text': "Useful websites and channels for IELTS, SAT and university admission:\n1) takeielts.britishcouncil.org\n2) ielts.org\n3) collegeboard.org\n4) khanacademy.org/sat\n5) ucas.com\n6) scholarshipportal.com\n7) studyportals.com\nYouTube: IELTS Liz, Magoosh, English with Lucy, E2 IELTS, College Info Geek.",
        'web_text': "The web app runs at localhost:8080. Open http://localhost:8080 in your browser to search questions, browse answers, and review resources.",
        'about_text': "This bot helps students with IELTS, SAT, and university information. Choose the correct section from the menu to get answers.\n\nThe bot works from a local database and does not require API keys.",
        'ask_email': "Please share your email address:",
        'question_not_found': "Sorry, I couldn't find that question. Please choose from the menu or try another wording.",
        'btn_back': "⬅️ Back",
        'settings_txt': "Settings menu. You can change your language:"
    },
    'ru': {
        'welcome': "Добро пожаловать! Пожалуйста, выберите язык:",
        'ask_name': "Начнем регистрацию. Введите имя и фамилию:",
        'ask_phone': "Отправьте номер телефона (Нажмите кнопку или введите):",
        'ask_loc': "Отправьте ваше местоположение или адрес:",
        'reg_success': "Вы успешно зарегистрировались! 🎉",
        'main_menu': "Главное меню. Выберите один из разделов:",
        'btn_phone': "📱 Отправить номер",
        'btn_sections': "📚 Разделы знаний (IELTS/SAT)",
        'btn_resources': "🌐 Ресурсы",
        'btn_web': "🌍 Web App",
        'btn_problem': "⚠️ Проблемы и предложения",
        'btn_settings': "⚙️ Настройки",
        'btn_about': "ℹ️ О боте",
        'btn_logout': "🚪 Выйти",
        'select_section': "По какому направлению вы хотите получить ответы?",
        'select_question': "Выберите один из вопросов:",
        'problem_prompt': "Что бы вы хотели добавить в бот? Есть ли жалобы? Напишите подробно:",
        'problem_received': "Спасибо! Ваше обращение отправлено администрации по электронной почте. 📬\nКопия также будет отправлена на ваш зарегистрированный адрес электронной почты, если он доступен.\nЕсли нужна дополнительная помощь, свяжитесь с админом:\nТел: 99 702 1775\nEmail: aslonovdiyorbek333@gmail.com",
        'resources_text': "Полезные сайты и каналы для IELTS, SAT и поступления в университет:\n1) takeielts.britishcouncil.org\n2) ielts.org\n3) collegeboard.org\n4) khanacademy.org/sat\n5) ucas.com\n6) scholarshipportal.com\n7) studyportals.com\nYouTube: IELTS Liz, Magoosh, English with Lucy, E2 IELTS, College Info Geek.",
        'web_text': "Веб-приложение работает на localhost:8080. Откройте http://localhost:8080 в браузере, чтобы искать вопросы, просматривать ответы и ресурсы.",
        'about_text': "Этот бот помогает студентам с IELTS, SAT и информацией о поступлении в университеты. Выберите нужный раздел из меню, чтобы получить ответы.\n\nБот работает на локальной базе данных и не требует API-ключей.",
        'ask_email': "Пожалуйста, введите ваш адрес электронной почты:",
        'question_not_found': "Извините, не удалось найти этот вопрос. Пожалуйста, выберите из меню или попробуйте другую формулировку.",
        'btn_back': "⬅️ Назад",
        'settings_txt': "Меню настроек. Вы можете изменить язык:"
    }
}

def get_main_keyboard(lang):
    return ReplyKeyboardMarkup([
        [STRINGS[lang]['btn_sections'], STRINGS[lang]['btn_resources']],
        [STRINGS[lang]['btn_web'], STRINGS[lang]['btn_about']],
        [STRINGS[lang]['btn_problem'], STRINGS[lang]['btn_settings']],
        [STRINGS[lang]['btn_logout']]
    ], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if user:
        context.user_data['lang'] = user[1]
        await update.message.reply_text(STRINGS[user[1]]['main_menu'], reply_markup=get_main_keyboard(user[1]))
        return MAIN_MENU
        
    keyboard = [['O\'zbekcha 🇺🇿', 'English 🇬🇧', 'Русский 🇷🇺']]
    await update.message.reply_text("Salom! / Hello! / Привет!", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True))
    return LANG

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    if 'O\'zbekcha' in text: lang = 'uz'
    elif 'English' in text: lang = 'en'
    else: lang = 'ru'
    
    context.user_data['lang'] = lang
    await update.message.reply_text(STRINGS[lang]['ask_name'], reply_markup=ReplyKeyboardRemove())
    return REG_NAME

async def reg_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['fullname'] = update.message.text
    lang = context.user_data['lang']
    
    btn = [[KeyboardButton(STRINGS[lang]['btn_phone'], request_contact=True)]]
    await update.message.reply_text(STRINGS[lang]['ask_phone'], reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True))
    return REG_PHONE

async def reg_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = update.message.text
        
    context.user_data['phone'] = phone
    lang = context.user_data['lang']
    
    btn = [[KeyboardButton("📍 Location", request_location=True)]]
    await update.message.reply_text(STRINGS[lang]['ask_loc'], reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True))
    return REG_LOCATION

async def reg_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.location:
        loc = f"{update.message.location.latitude}, {update.message.location.longitude}"
    else:
        loc = update.message.text
        
    context.user_data['location'] = loc
    lang = context.user_data['lang']

    await update.message.reply_text(STRINGS[lang]['ask_email'], reply_markup=ReplyKeyboardRemove())
    return REG_EMAIL

async def reg_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text
    context.user_data['email'] = email
    user_id = update.effective_user.id
    lang = context.user_data['lang']
    
    db.add_user(user_id, lang, context.user_data['fullname'], context.user_data['phone'], context.user_data['location'], email)
    
    await update.message.reply_text(STRINGS[lang]['reg_success'])
    await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
    return MAIN_MENU

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('lang', 'uz')
    
    if text == STRINGS[lang]['btn_sections']:
        keyboard = [
            ["IELTS", "SAT"],
            ["UNIVERSITIES", "TIME_MANAGEMENT"],
            ["STUDY_TIPS", "MOTIVATION"],
            ["DAILY_HABITS", "EXAM_ANXIETY"],
            ["AFTER_EXAM", "FOCUS"],
            ["RESOURCES_STUDY"],
            [STRINGS[lang]['btn_back']]
        ]
        await update.message.reply_text(STRINGS[lang]['select_section'], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return SECTION_VIEW
        
    elif text == STRINGS[lang]['btn_problem']:
        await update.message.reply_text(STRINGS[lang]['problem_prompt'], reply_markup=ReplyKeyboardMarkup([[STRINGS[lang]['btn_back']]], resize_keyboard=True))
        return PROBLEM_STATE
        
    elif text == STRINGS[lang]['btn_settings']:
        keyboard = [['O\'zbekcha 🇺🇿', 'English 🇬🇧', 'Русский 🇷🇺'], [STRINGS[lang]['btn_back']]]
        await update.message.reply_text(STRINGS[lang]['settings_txt'], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return SETTINGS_STATE

    elif text == STRINGS[lang]['btn_resources']:
        await update.message.reply_text(STRINGS[lang]['resources_text'])
        await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
        return MAIN_MENU

    elif text == STRINGS[lang]['btn_web']:
        await update.message.reply_text(STRINGS[lang]['web_text'])
        await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
        return MAIN_MENU

    elif text == STRINGS[lang]['btn_about']:
        await update.message.reply_text(STRINGS[lang]['about_text'])
        await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
        return MAIN_MENU

    elif text == STRINGS[lang]['btn_logout']:
        return await logout_handler(update, context)

    return MAIN_MENU

async def section_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('lang', 'uz')
    
    if text == STRINGS[lang]['btn_back']:
        await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
        return MAIN_MENU
        
    all_sections = ["IELTS", "SAT", "UNIVERSITIES", "TIME_MANAGEMENT", "STUDY_TIPS", "MOTIVATION", "DAILY_HABITS", "EXAM_ANXIETY", "AFTER_EXAM", "FOCUS", "RESOURCES_STUDY"]
    
    if text in all_sections:
        context.user_data['current_section'] = text
        questions = db.get_questions_by_section(text)
        
        if not questions:
            await update.message.reply_text("Hozircha bu bo'limda savollar yo'q.")
            return SECTION_VIEW
            
        keyboard = []
        for q in questions:
            q_text = q[1] if lang == 'uz' else (q[2] if lang == 'en' else q[3])
            keyboard.append([q_text])
        keyboard.append([STRINGS[lang]['btn_back']])
        
        await update.message.reply_text(STRINGS[lang]['select_question'], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return Q_VIEW

    return SECTION_VIEW

async def q_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('lang', 'uz')
    section = context.user_data.get('current_section')
    
    if text == STRINGS[lang]['btn_back']:
        keyboard = [
            ["IELTS", "SAT"],
            ["UNIVERSITIES", "TIME_MANAGEMENT"],
            ["STUDY_TIPS", "MOTIVATION"],
            ["DAILY_HABITS", "EXAM_ANXIETY"],
            ["AFTER_EXAM", "FOCUS"],
            ["RESOURCES_STUDY"],
            [STRINGS[lang]['btn_back']]
        ]
        await update.message.reply_text(STRINGS[lang]['select_section'], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return SECTION_VIEW
        
    questions = db.get_questions_by_section(section)
    for q in questions:
        q_text = q[1] if lang == 'uz' else (q[2] if lang == 'en' else q[3])
        if q_text == text:
            ans = db.get_answer_by_id(q[0])
            ans_text = ans[0] if lang == 'uz' else (ans[1] if lang == 'en' else ans[2])
            
            response = f"✨ *{section} - Info* ✨\n\n❓ *Q:* {q_text}\n\n💡 *A:* {ans_text}"
            await update.message.reply_text(response, parse_mode="Markdown")
            return Q_VIEW

    matched = db.find_question_by_text(section, text)
    if matched:
        ans = db.get_answer_by_id(matched[0])
        ans_text = ans[0] if lang == 'uz' else (ans[1] if lang == 'en' else ans[2])
        q_text = matched[1] if lang == 'uz' else (matched[2] if lang == 'en' else matched[3])
        response = (
            f"✨ *{section} - Info* ✨\n\n"
            f"❓ *Q:* {q_text}\n\n"
            f"💡 *A:* {ans_text}\n\n"
            f"📌 Agar sizga qo'shimcha ma'lumot kerak bo'lsa, iltimos boshqa bir savol bering yoki bo'limni qayta tanlang."
        )
        await update.message.reply_text(response, parse_mode="Markdown")
        return Q_VIEW
            
    await update.message.reply_text(STRINGS[lang]['question_not_found'])
    return Q_VIEW

async def problem_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('lang', 'uz')
    
    if text == STRINGS[lang]['btn_back']:
        await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
        return MAIN_MENU
        
    user_id = update.effective_user.id
    user_data = db.get_user(user_id)
    
    user_info = {
        'user_id': user_id,
        'fullname': user_data[2],
        'phone': user_data[3],
        'location': user_data[4],
        'email': user_data[5] if len(user_data) > 5 else None,
        'lang': user_data[1]
    }
    
    success = mailer.send_problem_email(user_info, text)
    if not success:
        await update.message.reply_text("Xat yuborilmadi. Iltimos, admin bilan bog'laning yoki email sozlamalarini tekshiring.")
    else:
        await update.message.reply_text(STRINGS[lang]['problem_received'])

    await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
    return MAIN_MENU

async def logout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    db.delete_user(user_id)
    context.user_data.clear()
    await update.message.reply_text("Siz muvaffaqiyatli logout qildingiz. /start ni bosing va qayta ro'yxatdan o'ting.")
    return ConversationHandler.END

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = context.user_data.get('lang', 'uz')
    
    if text == STRINGS[lang]['btn_back']:
        await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
        return MAIN_MENU
        
    if 'O\'zbekcha' in text: new_lang = 'uz'
    elif 'English' in text: new_lang = 'en'
    else: new_lang = 'ru'
    
    context.user_data['lang'] = new_lang
    user_id = update.effective_user.id
    user_data = db.get_user(user_id)
    email = user_data[5] if len(user_data) > 5 else None
    
    db.add_user(user_id, new_lang, user_data[2], user_data[3], user_data[4], email)
    
    await update.message.reply_text("Language updated! / Til o'zgardi! / Язык изменен!")
    await update.message.reply_text(STRINGS[new_lang]['main_menu'], reply_markup=get_main_keyboard(new_lang))
    return MAIN_MENU

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('lang', 'uz')
    await update.message.reply_text(STRINGS[lang]['about_text'])
    await update.message.reply_text(STRINGS[lang]['main_menu'], reply_markup=get_main_keyboard(lang))
    return MAIN_MENU

async def web_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = context.user_data.get('lang', 'uz')
    await update.message.reply_text(STRINGS[lang]['web_text'])
    return MAIN_MENU

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
            REG_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_name)],
            REG_PHONE: [MessageHandler(filters.TEXT | filters.CONTACT, reg_phone)],
            REG_LOCATION: [MessageHandler(filters.TEXT | filters.LOCATION, reg_location)],
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            SECTION_VIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, section_view)],
            Q_VIEW: [MessageHandler(filters.TEXT & ~filters.COMMAND, q_view)],
            PROBLEM_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, problem_handler)],
            SETTINGS_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, settings_handler)],
            ABOUT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, about_handler)],
            REG_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_email)],
        },
        fallbacks=[CommandHandler('start', start)],
    )
    
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('logout', logout_handler))
    app.add_handler(CommandHandler('web', web_handler))
    logger.info("Yirik ta'lim bot ishga tushmoqda...")
    app.run_polling()

if __name__ == '__main__':
    main()