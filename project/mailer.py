import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

# DIQQAT: Xavfsizlik uchun parollarni Environment Variable orqali bering!
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 465))
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "aslonovdiyorbek333@gmail.com")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "aslonovdiyorbek333@gmail.com")
# Google Account -> Security -> App Passwords orqali olingan maxsus parol kerak bo'ladi
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")

def send_problem_email(user_info, problem_text):
    if not SENDER_PASSWORD:
        logger.warning("Email paroli kiritilmagan, xat yuborilmadi.")
        return False
        
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ADMIN_EMAIL
    recipients = [ADMIN_EMAIL]

    user_email = user_info.get('email')
    if user_email and user_email != ADMIN_EMAIL:
        msg['Cc'] = user_email
        recipients.append(user_email)

    msg['Subject'] = f"⚠️ BOT PROBLEM REPORT: User {user_info['user_id']}"
    
    body = f"""
    Yangi murojaat tushdi:
    
    Foydalanuvchi ma'lumotlari:
    - ID: {user_info['user_id']}
    - Ism-Familiya: {user_info['fullname']}
    - Telefon: {user_info['phone']}
    - Manzil/Lokatsiya: {user_info['location']}
    - Email: {user_info.get('email', 'Noma\'lum')}
    - Tanlagan tili: {user_info['lang']}
    
    Murojaat / Muammo matni:
    --------------------------------------
    {problem_text}
    --------------------------------------
    """
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        logger.info("Email muvaffaqiyatli yuborildi.")
        return True
    except Exception as e:
        logger.error(f"Email yuborishda xatolik: {e}")
        return False