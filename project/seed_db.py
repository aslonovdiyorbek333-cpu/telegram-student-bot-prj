#!/usr/bin/env python3
"""Kengaytirilgan so'zlar va tesklar bilan database-ni to'ldirish."""

import database as db

# Database-ni ishga tushirish
db.init_db()

# Yangi bo'limlar va savollar
extended_questions = [
    # EXAM_ANXIETY Section
    ("EXAM_ANXIETY", "Stress Management",
     "Imtihon arafasida stressni qanday qabul qilish kerak?", "How to manage stress before exam?", "Как управлять стрессом перед экзаменом?",
     "Stressni qabul qiling - bu normal! Deep breathing: 4 daqiqaga nafas ol (4-hold-6-chiqar). 5-10 minut meditatsiya qil. YouTube: Headspace, Calm app foydalanishingiz mumkin. Kuniga 30 minut voleybol yoki futbol o'yna. Raqamli qurilmalardan 1 soat oldin uzoqlash - bu memory consolidation-ga yordam beradi. Ushbu usullar examen 1-2 kundan oldin ayniqsa samaralidir.",
     "Accept stress - it's normal! Deep breathing: inhale 4 sec (hold 4, exhale 6). Meditate 5-10 min. YouTube: Headspace, Calm app. Play volleyball or football 30 min daily. Stay away from phones 1 hour before sleep - this helps memory consolidation. These techniques are most effective 1-2 days before exam.",
     "Примите стресс - это нормально! Глубокое дыхание: вдыхаешь 4 сек (держи 4, выдыхаешь 6). Медитируй 5-10 минут. YouTube: Headspace, Calm app. Играй в волейбол или футбол 30 минут ежедневно. Держись подальше от телефонов за 1 час до сна - это помогает консолидации памяти. Эти техники наиболее эффективны за 1-2 дня до экзамена."),

    ("EXAM_ANXIETY", "Night Before Exam",
     "Imtihondan bir kun oldin nima qilish kerak?", "What to do the night before exam?", "Что делать ночь перед экзаменом?",
     "Imtihon kuni 20:00-da kitoblarni yopib, 21:00-da yotishga tayyorlaning. Yotishi 8-9 soat bo'lsin. Sabahda 1 soat oldin uyg'onish yaxshi - bu beyin-faol bo'lishiga vaqt beradi. Sabah ovqat: protein (tuxum, kolbasa) + carbs (plov, nan) + meva. Imtihon markaziga 30 minut oldin borishga tayyorlang - stress past bo'lmasa, birorta 5 minut o'qish afzaldir, lekin stressing ko'p bo'lsa, yura yoki dua qil.",
     "Close books by 8pm, prepare for bed by 9pm. Sleep 8-9 hours. Wake 1 hour before exam - gives brain time to activate. Morning breakfast: protein (eggs, sausage) + carbs (rice, bread) + fruit. Leave for exam center 30 min early. If not stressed, review 5 min before; if very stressed, walk or pray.",
     "Закрывайте книги к 20:00, готовьтесь ко сну к 21:00. Спите 8-9 часов. Просыпайтесь за 1 час до экзамена - это дает мозгу время активироваться. Завтрак: белок (яйца, колбаса) + углеводы (рис, хлеб) + фрукты. Уходите на 30 минут раньше. Если не стресс, повторите 5 минут перед; если очень стресс, прогуляйтесь или помолитесь."),

    ("EXAM_ANXIETY", "During Exam Tips",
     "Imtihon paytida qanday tibbiyot ishlatish kerak?", "What tips to follow during exam?", "Какие советы следовать во время экзамена?",
     "Imtihon paytida: 1) Har 30 minut o'rtasida 10 daqiqa break ol. 2) Suvni o'rta-o'rtaga iching. 3) Mushkul savollarga dastlab e'tibor bermang - oson savollarga o'ng turib davom eting. 4) Vaqt qoldi 5 minut bo'lganda, havotir olmang va hamma javoblarini yana ko'z yugurti. 5) Javoblarni shunisi qo'lib ko'ring - noto'g'ri javobga qaytmang. Misol: SAT Math uchun 45 minut ishlab, 2 minut break ol.",
     "During exam: 1) Take 10 min break every 30 min. 2) Drink water occasionally. 3) Skip difficult questions first - finish easy ones. 4) When 5 min left, don't panic, just review your answers. 5) Don't change answers unless very sure. Example: Work 45 min on SAT Math, 2 min break.",
     "Во время экзамена: 1) Делайте 10-минутный перерыв каждые 30 минут. 2) Пейте воду время от времени. 3) Сначала пропустите сложные вопросы - завершите легкие. 4) Когда осталось 5 минут, не паниковать, просто пересмотрите ответы. 5) Не меняйте ответы без уверенности. Пример: Работайте 45 минут на SAT Math, 2 минуты перерыва."),

    # AFTER_EXAM Section
    ("AFTER_EXAM", "Score Waiting",
     "Imtihon natijasi kutayotganda nima qilish kerak?", "What to do while waiting for exam results?", "Что делать во время ожидания результатов экзамена?",
     "Imtihon natijasini kutib turmasdan, o'zingizni bo'shqotiruvchi ish bilan band qiling. IELTS uchun 13 kun, SAT uchun 2-3 hafta kutish kerak. Bu vaqtda: yangi till o'rganing, kitob o'qiying, yangi hobbyni topish bilan harakat qiling. Stressing ko'paysa, psikholog bilan konsultatsiya qiling. Agar natija yomon bo'lsa, qaysi qismda xato bo'lganligi tahlil qiling va keyingi test uchun rejani tuzing.",
     "Don't wait idle for exam results. IELTS takes 13 days, SAT takes 2-3 weeks. Use this time: learn new language, read books, find new hobby. If stress increases, consult psychologist. If results are bad, analyze which part failed and plan for next test.",
     "Не ждите результаты в бездействии. IELTS занимает 13 дней, SAT занимает 2-3 недели. Используйте это время: учите новый язык, читайте книги, найдите новое хобби. Если стресс увеличивается, проконсультируйтесь с психологом. Если результаты плохие, проанализируйте, какая часть не сработала, и спланируйте следующий тест."),

    ("AFTER_EXAM", "Result Analysis",
     "Natija yomon chikdi, endi nima?", "My exam results were bad, what now?", "Мои результаты экзамена были плохие, что теперь?",
     "Natijani tahlil qiling: 1) Har qism balliga qarang. 2) Qaysi qism eng past? Listening/Reading/Writing/Speaking? 3) Agar SAT bo'lsa, Math yoki Reading past? 4) Qaysi xatoliklar tekrarilyapti? Misol: 'Listening-da 6 bo'ld, agar 1 hafta extra training qilsam, 7 bo'lar ekan' deb o'ylash. 5) Keyingi testga 6-8 hafta qo'ying, yangi usullarga harakat qiling. YouTube: IELTS/SAT tutoriallar ko'ring, gap osmon emas - millionlab odamlar 2-3 marta test qiladi va muvaffaq bo'ladi!",
     "Analyze your results: 1) Look at each section score. 2) Which section was lowest? Listening/Reading/Writing/Speaking? 3) If SAT, Math or Reading lower? 4) Which mistakes repeat? Example: 'Got Listening 6, if I train 1 week extra, I'll get 7'. 5) Schedule next test in 6-8 weeks, try new methods. Watch YouTube tutorials, it's not hopeless - millions retake 2-3 times and succeed!",
     "Проанализируйте результаты: 1) Посмотрите оценки по каждому разделу. 2) Какой раздел был самым низким? Listening/Reading/Writing/Speaking? 3) Если SAT, Math или Reading ниже? 4) Какие ошибки повторяются? Пример: 'Получил Listening 6, если тренироваться 1 неделю, получу 7'. 5) Запланируйте следующий тест на 6-8 недель, попробуйте новые методы. Смотрите YouTube-уроки, это не безнадежно - миллионы переаваивают 2-3 раза и добиваются успеха!"),

    # FOCUS Section
    ("FOCUS", "Concentration Techniques",
     "Uzun vaqt o'qida fokuslashni qanday qilish kerak?", "How to maintain focus while studying long hours?", "Как сохранить концентрацию при долгих часах учебы?",
     "Fokus saqlash uchun: 1) Telefonni boshqa xonaga qo'y. 2) Internet o'chirib qo'y yoki VPN ishlat. 3) Pomodoro: 25 min focus, 5 min break. 4) Bir xonani study zone qilg'in - faqatgina o'qish uchun. 5) Background music: lo-fi, classical, Focus@Will. 6) Healthy snacks: orikzak, apple, nuts. 7) Vaqt tracker qo'l: Toggl, TimeTree. Misol: Sabah 06:30-da 2 soat focus session qil (07:00 break), keyin 30 min break qil.",
     "To maintain focus: 1) Put phone in another room. 2) Turn off internet or use VPN blocker. 3) Pomodoro: 25 min focus, 5 min break. 4) Create study zone - only for studying. 5) Background music: lo-fi, classical, Focus@Will. 6) Healthy snacks: nuts, apple, raisins. 7) Time tracker: Toggl, TimeTree. Example: 6:30am do 2-hour focus session (break at 7am), then 30 min break.",
     "Чтобы сохранить фокус: 1) Положите телефон в другую комнату. 2) Выключите интернет или используйте блокиратор. 3) Pomodoro: 25 мин фокус, 5 мин перерыв. 4) Создайте учебную зону - только для учебы. 5) Фоновая музыка: lo-fi, классика, Focus@Will. 6) Здоровые закуски: орехи, яблоко, изюм. 7) Отслеживание времени: Toggl, TimeTree. Пример: 6:30 утра делать 2-часовую сессию фокуса (перерыв в 7 утра), затем 30-минутный перерыв."),

    ("FOCUS", "Avoid Burnout",
     "O'qish jarayonida burnout-dan qanday qochish kerak?", "How to avoid burnout during studies?", "Как избежать выгорания при обучении?",
     "Burnout-dan qochish: 1) Har hafta 1 kun complete break qol. 2) Kuniga kamida 8 soat uxla. 3) Haftada 3-4 marta sport qil. 4) Dushanba-juma: 2-3 soat study, shanba-yakshanba: 1-2 soat study. 5) Oyda 1 kuni butunlay bo'sh qil - do istana bor, do'stlar bilan chiqish. 6) Oyda 1 marta moto bilan safar qil, tabiatni ko'r. Burnout belgisi: 1) Motivation yo'q. 2) Har kuni charchalik. 3) Stress oshib ketdi. Agarda shuni sezsan, 3-5 kun butunlay rest qil va psikholog bilan gap.",
     "To avoid burnout: 1) Take one complete day off weekly. 2) Sleep at least 8 hours daily. 3) Exercise 3-4 times weekly. 4) Mon-Fri: 2-3 hour study, Sat-Sun: 1-2 hour study. 5) One day monthly completely off - visit parks, meet friends. 6) One road trip monthly. Burnout signs: 1) No motivation. 2) Daily tiredness. 3) Increased stress. If you notice, take 3-5 days complete rest and talk to psychologist.",
     "Чтобы избежать выгорания: 1) Возьмите один полный день отдыха в неделю. 2) Спите минимум 8 часов ежедневно. 3) Занимайтесь спортом 3-4 раза в неделю. 4) Пн-Пт: 2-3 часа учебы, Сб-Вс: 1-2 часа учебы. 5) Один день в месяц совсем свободный - парк, друзья. 6) Один переезд в месяц. Признаки выгорания: 1) Нет мотивации. 2) Ежедневная усталость. 3) Повышенный стресс. Если заметили, 3-5 дней полного отдыха и поговорите с психологом."),

    # RESOURCES_STUDY Section
    ("RESOURCES_STUDY", "Best Websites",
     "Eng yaxshi o'rganish saytlari qaysilari?", "What are the best study websites?", "Какие лучшие учебные сайты?",
     "IELTS: takeielts.britishcouncil.org (rasmiy), ielts.org (rasmiy), ieltsliz.com (video), esl-lab.com (Listening), engvid.com (video darslar). SAT: khan academy.org (rasmiy), collegeboard.org (rasmiy), magoosh.com (mashq), khan academy.org/sat (video). Universitetlar: ucas.com (Britaniya), commonapp.org (AQSh), educationusa.state.gov (AQSh), qsranking.com (ranking). Umumiy: britannica.com, ted.com, coursera.org. YouTube kanallar: IELTS Liz (IELTS), Mr. G (universities), Khan Academy (SAT).",
     "IELTS: takeielts.britishcouncil.org (official), ielts.org (official), ieltsliz.com (video), esl-lab.com (Listening), engvid.com (video lessons). SAT: khanacademy.org (official), collegeboard.org (official), magoosh.com (practice), khanacademy.org/sat (video). Universities: ucas.com (UK), commonapp.org (US), educationusa.state.gov (US), qsranking.com (ranking). General: britannica.com, ted.com, coursera.org. YouTube: IELTS Liz (IELTS), Mr. G (universities), Khan Academy (SAT).",
     "IELTS: takeielts.britishcouncil.org (официально), ielts.org (официально), ieltsliz.com (видео), esl-lab.com (Listening), engvid.com (видео-уроки). SAT: khanacademy.org (официально), collegeboard.org (официально), magoosh.com (практика), khanacademy.org/sat (видео). Университеты: ucas.com (UK), commonapp.org (US), educationusa.state.gov (US), qsranking.com (ranking). Общее: britannica.com, ted.com, coursera.org. YouTube: IELTS Liz (IELTS), Mr. G (universities), Khan Academy (SAT)."),
]

# Qo'shish
for question in extended_questions:
    conn = db._get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM QA_store WHERE section = ? AND question_uz = ?",
        (question[0], question[2])
    )
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO QA_store (section, category, question_uz, question_en, question_ru, answer_uz, answer_en, answer_ru)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', question)
    conn.commit()
    conn.close()

print("[OK] Database yangilandi! Ko'p bo'limlar qo'shildi.")
