# 🎓 Student Assistant & Automation Telegram Bot

<p align="center">
  <img src="https://img.shields.io/github/stars/aslonovdiyorbek333-cpu/telegram-student-bot-prj?style=for-the-badge&logo=github&color=34d399" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/aslonovdiyorbek333-cpu/telegram-student-bot-prj?style=for-the-badge&logo=github&color=60a5fa" alt="GitHub Forks">
  <img src="https://img.shields.io/github/license/aslonovdiyorbek333-cpu/telegram-student-bot-prj?style=for-the-badge&color=f472b6" alt="License">
</p>

<p align="center">
  <b>O'quvchilar uchun ta'lim jarayonini osonlashtiruvchi, vazifalarni avtomatlashtiruvchi va mustahkam backend arxitekturasiga ega zamonaviy Telegram bot loyihasi.</b>
</p>

---

## 🚀 Texnologiyalar Oliyasi (Tech Stack)

Loyihaning backend va ma'lumotlar qismi eng samarali texnologiyalar yordamida qurilgan:

* **Language:** ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) (Asosiy backend mantiq)
* **Database:** ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white) (Ma'lumotlarni saqlash va tezkor ishlash)
* **Web Framework:** ![Web App](https://img.shields.io/badge/Web_App-F57C00?style=flat-square&logo=javascript&logoColor=white) (Webhook va integratsiyalar uchun)
* **Environment:** ![Dotenv](https://img.shields.io/badge/.env-Active-brightgreen?style=flat-square) (Xavfsizlik va maxfiy kalitlar)

---

## 📁 Loyiha Strukturasi (Project Tree)

```text
├── project/
│   ├── web/                # Web interfeys va static fayllar (app.js, index.html, style.css)
│   ├── bot_data.db         # SQLite ma'lumotlar bazasi
│   ├── bot.py              # Botning asosiy mantiqiy kodlari
│   ├── database.py         # DB bilan ishlash: ulanish, jadvallar yaratish va SQL so'rovlar
│   ├── mailer.py           # Avtomatlashtirilgan xabarlar (Email/Xabarnomalar) yuborish tizimi
│   ├── run_bot.py          # Loyihani ishga tushiruvchi asosiy nuqta (Main entry)
│   ├── seed_db.py          # Baza uchun boshlang'ich sinov ma'lumotlarini (dummy data) yaratish
│   └── web_app.py          # Web ilova qismi (API yoki Webhook sozlamalari)
├── .env                    # Maxfiy tokenlar va sozlamalar (Lokalda qoladi)
├── .gitignore              # GitHub-ga chiqmaydigan fayllar ro'yxati
└── requirements.txt        # Zaruriy kutubxonalar ro'yxati

✨ Asosiy Imkoniyatlar (Features)

* 📦 Modulli Arxitektura: Har bir qism (database, mailer, web_app) alohida modullarga ajratilgan bo'lib, loyihani kengaytirishni osonlashtiradi.
* 💾 Ma'lumotlar Integratsiyasi: database.py orqali SQLite bazasi mukammal boshqariladi.
* 📧 Mailer Tizimi: Foydalanuvchilarga bildirishnomalar va xabarlarni avtomatik yetkazish.
* 🌐 Web App Qo'llab-quvvatlovi: Botni tashqi dunyo bilan Webhook yoki API orqali bog'lash imkoniyati.

🛠️ Lokal Muhitda Ishga Tushirish

Loyihani o'z kompyuteringizda sinab ko'rish uchun quyidagi qadamlarni bering:

1. Repozitoriyani yuklab oling:
   git clone [https://github.com/aslonovdiyorbek333-cpu/telegram-student-bot-prj.git](https://github.com/aslonovdiyorbek333-cpu/telegram-student-bot-prj.git)
   cd telegram-student-bot-prj

2. Virtual muhitni yoqing va kutubxonalarni o'rnating:
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac uchun
   .venv\Scripts\activate     # Windows uchun
   pip install -r requirements.txt

3. Konfiguratsiyani sozlang:
   .env faylini ochib, o'zingizning bot tokenlaringizni kiriting.

4. Baza ma'lumotlarini yuklash va botni ishga tushirish:
   python project/seed_db.py  # Bazani to'ldirish
   python project/run_bot.py  # Botni boshlash


   👨‍💻 Dasturchi va Aloqa (Developer Info)
Loyiha bo'yicha takliflar, savollar yoki hamkorlik uchun quyidagi aloqa kanallari orqali bog'lanishingiz mumkin:

Dasturchi: Diyorbek

📧 Email: aslonovdiyorbek333@gmail.com

📞 Telefon: +998 (99) 702-17-75

🌐 GitHub: aslonovdiyorbek333-cpu

💡 Murojaat uchun: Agarda sizga ham shunday professional turdagi Python Telegram botlar kerak bo'lsa, menga murojaat qiling! Yuqori sifat va mukammal backend kafolatlanadi.

📝 Litsenziya
Ushbu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot LICENSE faylida.