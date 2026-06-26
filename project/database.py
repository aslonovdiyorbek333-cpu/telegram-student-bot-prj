import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "bot_data.db"

def _get_connection():
    return sqlite3.connect(str(DB_PATH))


def init_db():
    conn = _get_connection()
    cursor = conn.cursor()
    
    # Foydalanuvchilar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            lang TEXT,
            fullname TEXT,
            phone TEXT,
            location TEXT,
            email TEXT,
            reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    if 'email' not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
    
    # Savollar va javoblar jadvali
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QA_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT,
            category TEXT,
            question_uz TEXT,
            question_en TEXT,
            question_ru TEXT,
            answer_uz TEXT,
            answer_en TEXT,
            answer_ru TEXT
        )
    ''')
    
    # Bazani boshlang'ich ma'lumotlar bilan to'ldirish
    default_questions = [
        # TIME MANAGEMENT Section
        ("TIME_MANAGEMENT", "Planning",
         "Imtihonlarga tayyorlanish uchun vaqtni qanday bo'lajak?", "How to plan your time for exam preparation?", "Как планировать время для подготовки к экзаменам?",
         "Tayyorlanish uchun 10-12 hafta bo'yicha rejalash qiling. Har hafta 3-4 mavzuni o'rganing, 1-2 test ishlang. Misol: IELTS uchun 1-hafta Listening, 2-hafta Reading, 3-hafta Writing. Excel yoki Google Calendar da jadval tuzing. Har kun 2-3 soat mashq qiling. Sayt: studyplan.com, Notion template-lar.",
         "Plan 10-12 weeks for preparation. Study 3-4 topics per week and complete 1-2 tests. Example: Week 1 Listening, Week 2 Reading, Week 3 Writing for IELTS. Create a schedule in Excel or Google Calendar. Practice 2-3 hours daily. Resources: studyplan.com, Notion templates.",
         "Планируйте 10-12 недель подготовки. Изучайте 3-4 темы в неделю и выполняйте 1-2 теста. Пример: Неделя 1 Listening, Неделя 2 Reading, Неделя 3 Writing для IELTS. Создайте расписание в Excel или Google Calendar. Занимайтесь 2-3 часа ежедневно. Ресурсы: studyplan.com, Notion templates."),

        ("TIME_MANAGEMENT", "Daily Routine",
         "Kunlik o'rganish jadvali qanday bo'lishi kerak?", "What should a daily study schedule look like?", "Как должно выглядеть ежедневное расписание занятий?",
         "Kunlik jadval: 08:00 Listening 30 min, 08:30 Break 10 min, 08:40 Reading 45 min, 09:25 Break 15 min, 09:40 Writing 45 min, 10:25 Break 10 min, 10:35 Speaking 30 min. Shuni hisobga olib, har 45 minutdan so'ng 10-15 minutlik tanaffus qiling. Hamma vaqt boshqacha narsalarni o'rganing. Resurs: Forest app (fokus uchun).",
         "Daily schedule: 8:00 Listening 30 min, 8:30 Break 10 min, 8:40 Reading 45 min, 9:25 Break 15 min, 9:40 Writing 45 min, 10:25 Break 10 min, 10:35 Speaking 30 min. Take 10-15 min breaks every 45 minutes. Vary your learning each time. Resource: Forest app (for focus).",
         "Ежедневное расписание: 8:00 Listening 30 мин, 8:30 Перерыв 10 мин, 8:40 Reading 45 мин, 9:25 Перерыв 15 мин, 9:40 Writing 45 мин, 10:25 Перерыв 10 мин, 10:35 Speaking 30 мин. Делайте перерывы 10-15 минут каждые 45 минут. Варьируйте обучение. Ресурс: Forest app (для сосредоточения)."),

        ("TIME_MANAGEMENT", "Exam Day",
         "Imtihon kuni qanday vaqt boshqarish kerak?", "How to manage time on exam day?", "Как управлять временем в день экзамена?",
         "Imtihon kuni 1 soat oldin imtihon markaziga yozing. O'z vaqtingizni har qismda tekshiring: IELTS Reading uchun har passage 15-17 minut, SAT Math uchun shunarsa qiyin masala uchun 45-60 daqiqa. Dastlab oson savollarni javob bering, keyin murakkablarni qiling. Vaqt tugatilish 5 minutdan oldin javoblarini yana bir bor tekshiring.",
         "Come 1 hour before the exam time. Manage your time for each part: IELTS Reading 15-17 min per passage, SAT Math 45-60 sec per hard problem. Answer easy questions first, then hard ones. Check your answers 5 minutes before time ends.",
         "Приходите на 1 час раньше времени экзамена. Управляйте временем для каждой части: IELTS Reading 15-17 минут за проход, SAT Math 45-60 секунд за сложную задачу. Ответьте на легкие вопросы сначала, затем на сложные. Проверьте ответы за 5 минут до конца."),

        # STUDY TIPS Section
        ("STUDY_TIPS", "Effective Methods",
         "Samarali o'rganish usullari nima?", "What are effective study methods?", "Какие эффективные методы обучения?",
         "Eng samarali usullar: Pomodoro (25 min ishlash, 5 min tanaffus), Spaced Repetition (tez unutish degani xolis), Mind Mapping (fikrlarni sxemalantirib tuzing), Active Recall (javoblarini yopib yozing). Misol: IELTS uchun 3 marta bir passage o'qing: 1-kun bir marta, 2-kun keyin yana, hafta keyingi yana. Kitoblar: 'Make It Stick' by Brown.",
         "Most effective methods: Pomodoro (25 min work, 5 min break), Spaced Repetition (repeat after forgetting), Mind Mapping (diagram your ideas), Active Recall (cover and write answers). Example: Read an IELTS passage 3 times: day 1, 2 days later, week later. Books: 'Make It Stick' by Brown.",
         "Самые эффективные методы: Pomodoro (25 мин работы, 5 мин перерыва), Spaced Repetition (повторяйте после забывания), Mind Mapping (диаграммируйте идеи), Active Recall (закройте и напишите ответы). Пример: Прочитайте отрывок IELTS 3 раза: день 1, 2 дня спустя, неделю спустя. Книги: 'Make It Stick' by Brown."),

        ("STUDY_TIPS", "Vocabulary Building",
         "So'zlarni samarali o'qishing nimaga?", "How to build vocabulary effectively?", "Как эффективно расширять словарь?",
         "Kuniga 10-20 yangi so'z o'rganing. Quizlet, Anki kabi fleshocard aplikatsiyalarni ishlating. Har so'zni 5 ta gapda ishlatib ko'ring. Kitoblarni o'qiganda, fanfilmlar ko'riganda yoki podcastlarni tinglaganda yangi so'zlarni yozing. Misol: 'Ambiguous' so'zini: 1) Definisyon o'qing. 2) 3 gapda ishlatamiz. 3) Sinonimlarni (unclear, vague) yozamiz. 4) Antonimlari (clear) yozamiz. Sayt: vocabulary.com, learnenglish.britishcouncil.org.",
         "Learn 10-20 new words per day. Use flashcard apps like Quizlet and Anki. Use each word in 5 sentences. Write new words while reading books, watching films, or listening to podcasts. Example: 'Ambiguous': 1) Read definition. 2) Use in 3 sentences. 3) Write synonyms (unclear, vague). 4) Write antonyms (clear). Websites: vocabulary.com, learnenglish.britishcouncil.org.",
         "Изучайте 10-20 новых слов в день. Используйте приложения для карточек, как Quizlet и Anki. Используйте каждое слово в 5 предложениях. Записывайте новые слова при чтении, просмотре фильмов или прослушивании подкастов. Пример: 'Ambiguous': 1) Прочитайте определение. 2) Используйте в 3 предложениях. 3) Напишите синонимы (unclear, vague). 4) Напишите антонимы (clear). Сайты: vocabulary.com, learnenglish.britishcouncil.org."),

        ("STUDY_TIPS", "Practice Tests",
         "Amaliyot testlari qanchalik muhim?", "How important are practice tests?", "Насколько важны пробные тесты?",
         "Amaliyot testlari juda muhim! Haftalik 1-2 test ishlang. IELTS uchun rasmiy Cambridge IELTS 1-18 kitoblarni, SAT uchun Khan Academy testlarni, UNI uchun real exam testlarini ishlang. Har test keyin natijalarini tahlil qiling: qaysi savollarni noto'g'ri javob berdim? Nima o'rgandim? Keyingi testda yaxshiroq natijavermaman? Timing berish ham muhim: test vaqtida o'zingizni toriqlik bilan tugatadizbini ko'ring.",
         "Practice tests are very important! Do 1-2 tests weekly. For IELTS use official Cambridge IELTS books 1-18, for SAT use Khan Academy tests, for universities use real exam papers. Analyze each test: which questions did I answer wrong? What did I learn? Will I do better next test? Also practice timing: see if you finish within the time limit.",
         "Пробные тесты очень важны! Выполняйте 1-2 теста в неделю. Для IELTS используйте официальные книги Cambridge IELTS 1-18, для SAT используйте Khan Academy тесты, для университетов используйте реальные экзаменационные работы. Анализируйте каждый тест: какие вопросы я ответил неправильно? Что я узнал? Буду ли я лучше в следующем тесте? Также тренируйте управление временем: посмотрите, закончите ли вы в отведенное время."),

        # MOTIVATION Section
        ("MOTIVATION", "Long Term Goals",
         "Uzoq muddatli maqsadlar qanday qo'yish kerak?", "How to set long-term goals?", "Как устанавливать долгосрочные цели?",
         "SMART maqsadlar qo'ying: Specific (aniq), Measurable (o'lchash mumkin), Achievable (erishish mumkin), Relevant (tegishli), Time-bound (muddatbadihii). Misol: 'IELTS 7.0 to'plamini Iyun 2026 da olish' emas balki 'Listening 8, Reading 7, Writing 6.5, Speaking 7'. Oylik sub-maqsadlar qo'ying. Hanafi oyiga 1000 yangi so'z o'rganing. Har hafta 2 Writing essay yozamiz. Maqsadlarni duvari yoki kompyuterga yapistiring, har kun ko'ring. Motivasyon video-bloglari: TEDx, Andrew Huberman.",
         "Set SMART goals: Specific, Measurable, Achievable, Relevant, Time-bound. Example: Not 'Get IELTS 7.0 by June 2026' but 'Listening 8, Reading 7, Writing 6.5, Speaking 7'. Set monthly sub-goals. Learn 1000 new words each month. Write 2 Writing essays weekly. Put your goals on a wall or computer, check daily. Motivation video blogs: TEDx, Andrew Huberman.",
         "Устанавливайте SMART-цели: Specific, Measurable, Achievable, Relevant, Time-bound. Пример: Не 'Получить IELTS 7.0 к июню 2026', а 'Listening 8, Reading 7, Writing 6.5, Speaking 7'. Устанавливайте ежемесячные подцели. Изучайте 1000 новых слов каждый месяц. Пишите 2 эссе для Writing в неделю. Повесьте свои цели на стену или компьютер, проверяйте ежедневно. Видео-блоги мотивации: TEDx, Andrew Huberman."),

        ("MOTIVATION", "Overcoming Failure",
         "Muvaffaqiyatsizlik va to'satdan balandligini qanday hal qilish kerak?", "How to overcome failure and setbacks?", "Как преодолеть неудачу и спады?",
         "Har kishi tanaga tushadi. IELTS testda 6.0 olyapti, keyin 5.5 olyapti - bu normal! Nima bo'ldi? Test 1da Reading-da xush boshlagan-ekan, Test 2da Reading qimmat bo'lgan? Shunga fokus berish kerak. Test 1dagi bilimlari yo'q ketgan emas! Keyingi test 2 hafta keyin bo'lsin, o'z vaqtingiz bor. Har kun 1 muvaffaqiyatni yozing - 'Bugun 10ta IELTS Listening savol to'g'ri javob berdim', 'Bugun 1000 so'z o'rgandim'. Psychologist consultation ishlaning agar stressing ko'paysa. Sayt: psychologytoday.com counselor topish uchun.",
         "Everyone fails. You got IELTS 6.0, then 5.5 on next test - that's normal! What happened? Test 1 Reading was good, Test 2 Reading was hard? Focus on that. Your knowledge from Test 1 didn't disappear! Your next test is in 2 weeks, you have time. Write one success daily - 'Today I answered 10 IELTS Listening correctly', 'Today I learned 1000 words'. See a psychologist if stress increases. Website: psychologytoday.com to find counselor.",
         "Все падают. Вы получили IELTS 6.0, затем 5.5 на следующем тесте - это нормально! Что произошло? На тесте 1 Reading был хорош, на тесте 2 Reading был сложный? Сосредоточьтесь на этом. Ваши знания от теста 1 не исчезли! Ваш следующий тест через 2 недели, у вас есть время. Напишите один успех ежедневно - 'Сегодня я правильно ответил на 10 вопросов IELTS Listening', 'Сегодня я выучил 1000 слов'. Обратитесь к психологу, если стресс усиливается. Веб-сайт: psychologytoday.com для поиска консультанта."),

        # DAILY HABITS Section
        ("DAILY_HABITS", "Morning Routine",
         "Ertalabki rejasi qanday bo'lishi kerak o'quvchilar uchun?", "What should a student's morning routine be?", "Какой должна быть утренняя рутина студента?",
         "Ertalabki rejasi: 6:30 Uyg'on, 6:40 Suv iching, 6:50 Sport (jog yoki yoga) 20 min, 7:10 Dush, 7:30 Nonushta, 7:50 30 min Listening o'rganing, 8:20 Mektepga/universitetga bor. Ertalabgi sport energiya beradi, Listening tinglovchi 'warm up' bo'ladi. Misol: IELTS listening BBC News 30 minut. Sayt: Nike Training Club app (yoga, jog uchun).",
         "Morning routine: 6:30 Wake up, 6:40 Drink water, 6:50 Exercise (jog or yoga) 20 min, 7:10 Shower, 7:30 Breakfast, 7:50 Study Listening 30 min, 8:20 Go to school/university. Morning exercise gives energy, Listening is a warm-up. Example: IELTS Listening BBC News 30 min. Website: Nike Training Club app (yoga, jogging).",
         "Утренняя рутина: 6:30 Проснитесь, 6:40 Пейте воду, 6:50 Упражнения (бег или йога) 20 мин, 7:10 Душ, 7:30 Завтрак, 7:50 Учите Listening 30 мин, 8:20 Идите в школу/университет. Утренние упражнения дают энергию, Listening — это разминка. Пример: IELTS Listening BBC News 30 мин. Веб-сайт: Nike Training Club app (йога, бег)."),

        ("DAILY_HABITS", "Evening Study",
         "Oqshom o'rganish rejasi nimaga?", "What should evening study look like?", "Как должны выглядеть вечерние занятия?",
         "Oqshom saat 18:00-dan 20:00 gacha o'rganish. 18:00 Nonushta, 18:20 Reading yoki Writing 40 min, 19:00 Break 10 min, 19:10 Speaking or Math 40 min, 19:50 Break 10 min, 20:00 Test yoki amaliyot. Oqshom o'rganish to'satdan ertalabki o'rganishdan qismatan ozbek bo'ladi - buning sababy ko'zlar ham charchaladi. Agar oqshom 20:00 dan keyin o'qri bo'lsangiz, 1-2 soat uza olmasingiz, bu xalosma. Sayt: Productive app (time tracking).",
         "Evening study from 6pm-8pm. 6:00 Snack, 6:20 Reading or Writing 40 min, 7:00 Break 10 min, 7:10 Speaking or Math 40 min, 7:50 Break 10 min, 8:00 Test or practice. Evening study is harder than morning - eyes are tired. If you study after 8pm and can't finish in 1-2 hours, it's okay. Website: Productive app (time tracking).",
         "Вечерние занятия с 18:00 до 20:00. 18:00 Перекус, 18:20 Reading или Writing 40 мин, 19:00 Перерыв 10 мин, 19:10 Speaking или Math 40 мин, 19:50 Перерыв 10 мин, 20:00 Тест или практика. Вечерние занятия сложнее, чем утренние - глаза устали. Если вы занимаетесь после 20:00 и не можете закончить за 1-2 часа, это нормально. Веб-сайт: Productive app (отслеживание времени)."),

        # IELTS Section (expanded)
        ("IELTS", "General",
         "IELTS o'zi nima?", "What is IELTS?", "What is IELTS?",
         "IELTS - xalqaro ingliz tili imtihoni bo'lib, o'qish, ish va immigratsiya uchun ishlatiladi. U Listening, Reading, Writing va Speaking bo'limlaridan iborat. Tayyorlanishda rasmiy British Council va IDP materiallarini, IELTS Liz va Magoosh YouTube kanallarini, shuningdek Cambridge IELTS kitoblarini ishlating.",
         "IELTS is the international English test used for study, work, and migration. It includes Listening, Reading, Writing, and Speaking. Prepare with official British Council and IDP materials, IELTS Liz and Magoosh YouTube channels, and Cambridge IELTS books.",
         "IELTS — это международный тест по английскому для учебы, работы и миграции. Он включает Listening, Reading, Writing и Speaking. Готовьтесь с официальными материалами British Council и IDP, каналами IELTS Liz и Magoosh и книгами Cambridge IELTS."),

        ("IELTS", "Structure",
         "IELTS imtihoni necha qismdan iborat?", "How many parts are in IELTS?", "Из каких частей состоит IELTS?",
         "IELTS imtihoni 4 qismdan iborat: Listening, Reading, Writing va Speaking. Listening 30 daqiqa, Reading 60 daqiqa, Writing 60 daqiqa va Speaking 11-14 daqiqa davom etadi. Har bir qismga alohida tayyorgarlik qiling va rasmiy sample testlardan foydalaning.",
         "The IELTS test has 4 parts: Listening, Reading, Writing, and Speaking. Listening is 30 minutes, Reading is 60 minutes, Writing is 60 minutes, and Speaking is 11-14 minutes. Prepare separately for each part and use official sample tests.",
         "Экзамен IELTS состоит из 4 частей: Listening, Reading, Writing и Speaking. Listening — 30 минут, Reading — 60 минут, Writing — 60 минут, Speaking — 11-14 минут. Готовьтесь к каждой части отдельно и используйте официальные образцы тестов."),

        ("IELTS", "Listening",
         "Listening bo'limiga qanday tayyorlanish kerak?", "How to prepare for IELTS Listening?", "Как подготовиться к IELTS Listening?",
         "Listening uchun har kuni audio tinglang: BBC Learning English, TED Talks, IELTS Liz va English with Lucy kanallarini ishlating. Test paytida kalit so'zlarni topish, spikerlar o'rtasidagi ohang o'zgarishini payqash va javob formatiga rioya qilish muhim. Rasmiy resurslar: takeielts.britishcouncil.org va ielts.org.",
         "For IELTS Listening, listen to audio everyday: BBC Learning English, TED Talks, IELTS Liz, and English with Lucy. During the test, identify keywords, speaker changes, and answer format. Official resources are takeielts.britishcouncil.org and ielts.org.",
         "Для IELTS Listening слушайте аудио ежедневно: BBC Learning English, TED Talks, IELTS Liz и English with Lucy. На экзамене определяйте ключевые слова, смену говорящего и формат ответов. Официальные ресурсы — takeielts.britishcouncil.org и ielts.org."),

        ("IELTS", "Reading",
         "Reading bo'limida qanday usul qo'llash kerak?", "What is the best approach for IELTS Reading?", "Какой лучший подход к IELTS Reading?",
         "Reading bo'limida skimming va scanning usullarini ishlating: avval tezda matnni o'qing, keyin savollarga qayting. Har bir passage uchun asosiy g'oyani toping va savollarni matndan izlang. Rasmiy testlar uchun IELTS.org, British Council va IELTS Liz saytlariga qarang.",
         "Use skimming and scanning in IELTS Reading: first read the passage quickly, then return to the questions. Identify the main idea for each passage and locate answers in the text. Refer to IELTS.org, British Council, and IELTS Liz for official practice.",
         "В IELTS Reading используйте скимминг и сканирование: сначала быстро прочитайте текст, затем вернитесь к вопросам. Определяйте основную идею каждого текста и ищите ответы в тексте. Обратитесь к IELTS.org, British Council и IELTS Liz для официальной практики."),

        ("IELTS", "Writing",
         "Writing bo'limida qanday xatoliklar ko'p uchraydi?", "What are common mistakes in IELTS Writing?", "Какие распространенные ошибки в IELTS Writing?",
         "Ko'p uchraydigan xatoliklar: topshiriqni noto'g'ri tushunish, so'z sonini oshirib yuborish, grammatik va imlo xatolari, paragraf tuzilmasini buzish va fikrlarni chalkashtirib yozish. Har doim rejani yozing, kirish, ikki tana paragrafi va xulosani aniq bayon qiling. Resurslar: IELTS Liz, IELTS Advantage va Grammarly bloglari.",
         "Common mistakes are misunderstanding the task, exceeding the word count, grammar and spelling errors, poor paragraph structure, and unclear ideas. Always write a plan, use an introduction, two body paragraphs and a clear conclusion. Resources include IELTS Liz, IELTS Advantage, and Grammarly blogs.",
         "Распространенные ошибки: неправильное понимание задания, превышение лимита слов, ошибки грамматики и орфографии, плохая структура абзацев и неясные мысли. Всегда планируйте письмо, используйте введение, два основных абзаца и четкое заключение. Ресурсы: IELTS Liz, IELTS Advantage, Grammarly."),

        ("IELTS", "Speaking",
         "Speaking qismiga qanday tayyorlanish kerak?", "How to prepare for IELTS Speaking?", "Как подготовиться к IELTS Speaking?",
         "Speaking uchun eng yaxshi usul — mavzular ro'yxatini tuzish va kundalik gapirishni mashq qilish. IELTS Liz, E2 IELTS va EngVid kanallaridan real test namunalarini tinglang. O'z nutqingizni yozib eshiting, talaffuz va intonatsiyaga e'tibor bering. Gaplaringizni aniq va to'g'ri tuzishga harakat qiling.",
         "The best way to prepare for IELTS Speaking is to list topics and practice speaking daily. Listen to real test samples from IELTS Liz, E2 IELTS, and EngVid. Record your speech, pay attention to pronunciation and intonation, and try to speak clearly and accurately.",
         "Лучший способ подготовиться к IELTS Speaking — составить список тем и ежедневно практиковаться в разговоре. Слушайте реальные примеры тестов на IELTS Liz, E2 IELTS и EngVid. Записывайте свою речь, обращайте внимание на произношение и интонацию, старайтесь говорить ясно и точно."),

        ("IELTS", "Booking",
         "IELTSni qanday buyurtma qilaman?", "How to book IELTS?", "Как записаться на IELTS?",
         "IELTSni buyurtma qilish uchun rasmiy saytga kirib, test markazini va sanani tanlang. TakeIELTS, British Council va IDP saytlari orqali ro'yxatdan o'ting, to'lovni onlayn bajaring va tasdiqlovchi xatni saqlang. Har doim test markaziga hujjatlarni olib boring.",
         "To book IELTS, go to the official site, choose a test center and date. Register through TakeIELTS, British Council, or IDP, pay online, and save the confirmation email. Always bring your documents to the test center.",
         "Чтобы записаться на IELTS, зайдите на официальный сайт, выберите тестовый центр и дату. Зарегистрируйтесь через TakeIELTS, British Council или IDP, оплатите онлайн и сохраните подтверждение. Всегда берите документы с собой в центр тестирования."),

        ("IELTS", "Resources",
         "QLearning uchun qanday saytlar va kanallar foydali?", "Which websites and channels are useful for IELTS?", "Какие сайты и каналы полезны для IELTS?",
         "IELTS uchun eng yaxshi resurslar: takeielts.britishcouncil.org, ielts.org, ieltsliz.com, Magoosh va BBC Learning English. YouTube kanallari: IELTS Liz, E2 IELTS, English with Lucy va Learn English with Emma. Bu resurslar bilan test formatini o'rganing, sample testlar yeching va tayyorlanish rejasi tuzing.",
         "The best IELTS resources are takeielts.britishcouncil.org, ielts.org, ieltsliz.com, Magoosh, and BBC Learning English. YouTube channels: IELTS Liz, E2 IELTS, English with Lucy, Learn English with Emma. Use these resources to learn the format, do sample tests, and create a study plan.",
         "Лучшие ресурсы для IELTS: takeielts.britishcouncil.org, ielts.org, ieltsliz.com, Magoosh и BBC Learning English. Каналы YouTube: IELTS Liz, E2 IELTS, English with Lucy, Learn English with Emma. Используйте эти ресурсы, чтобы изучить формат, практиковаться и составить план подготовки."),

        # SAT Section
        ("SAT", "General",
         "SAT imtihoni nima uchun topshiriladi?", "Why take the SAT?", "Зачем сдавать SAT?",
         "SAT AQSh va boshqa xalqaro universitetlarga kirish uchun muhim test hisoblanadi. U akademik qobiliyatning asosiy yo'nalishlarini tekshiradi va ba'zi stipendiya dasturlarida ham talab qilinadi. Tayyorlanishda College Board rasmiy sayti, Khan Academy va Magoosh resurslaridan foydalaning.",
         "The SAT is an important test for admission to US and international universities. It checks core academic skills and is required for some scholarships. Prepare with the official College Board site, Khan Academy, and Magoosh.",
         "SAT — это важный тест для поступления в вузы США и мира. Он проверяет ключевые академические навыки и требуется для некоторых стипендий. Готовьтесь с официального сайта College Board, Khan Academy и Magoosh."),

        ("SAT", "Structure",
         "SAT necha qismdan iborat?", "How many sections are in the SAT?", "Сколько разделов в SAT?",
         "SAT ikki asosiy bo'limdan iborat: Evidence-Based Reading and Writing (EBRW) va Math. EBRW ichida Reading va Writing & Language bo'limlari bor. Math bo'limida kalkulyatorli va kalkulyatorsiz bloklar mavjud. Rasmiy College Board testlari sizga formatni yaxshiroq tushunishga yordam beradi.",
         "The SAT has two main sections: Evidence-Based Reading and Writing (EBRW) and Math. EBRW includes Reading and Writing & Language. Math has calculator and no-calculator blocks. Official College Board tests help you understand the format.",
         "SAT состоит из двух основных разделов: Evidence-Based Reading and Writing (EBRW) и Math. EBRW включает Reading и Writing & Language. Math содержит блоки с калькулятором и без. Официальные тесты College Board помогают понять формат."),

        ("SAT", "Reading",
         "SAT Reading bo'limida qanday ishlash kerak?", "How to perform well in SAT Reading?", "Как хорошо выступить в SAT Reading?",
         "Reading bo'limida har bir matn uchun asosiy fikrni tez toping, so'ng savolga qayting va javobni to'g'ridan-to'g'ri matndan oling. Hech qachon taxmin qilib yozmang. Amaliyot uchun Khan Academy, PrepScholar va College Board rasmiy resurslarini ishlating.",
         "In SAT Reading, quickly identify the main idea for each passage, return to the question, and find the answer directly in the text. Never guess. Practice with Khan Academy, PrepScholar, and official College Board resources.",
         "В SAT Reading быстро определяйте основную мысль каждого текста, возвращайтесь к вопросам и ищите ответ прямо в тексте. Никогда не угадывайте. Практикуйтесь с Khan Academy, PrepScholar и официальными ресурсами College Board."),

        ("SAT", "Math",
         "SAT Math uchun qanday strategiyalar bor?", "What strategies are there for SAT Math?", "Какие стратегии есть для SAT Math?",
         "Math bo'limida formulalarni yaxshi yodlang, tez hisoblashni mashq qiling va avval oson savollarga o'ting. Qiyin masalalarni keyinroq qoldiring. Resurslar: Khan Academy SAT Math, PWN Test Prep, va College Board official practice.",
         "For SAT Math, memorize formulas, practice quick calculations, and start with easy questions. Leave hard problems for later. Use Khan Academy SAT Math, PWN Test Prep, and College Board official practice.",
         "Для SAT Math выучите формулы, тренируйте быстрые вычисления и начинайте с легких задач. Оставляйте сложные задачи на потом. Используйте Khan Academy SAT Math, PWN Test Prep и официальные практики College Board."),

        ("SAT", "Essay",
         "SAT essay yozish kerakmi?", "Is the SAT essay required?", "Нужно ли писать эссе на SAT?",
         "Ko'p universitetlar endi SAT essayni majburiy emas deb hisoblaydi, lekin ba'zi dasturlar talab qilishi mumkin. Agar kerak bo'lsa, kuchli kirish, ikki-uch asosiy fikr va aniq xulosa yozing. Rasmiy yo'riqnomalar uchun College Board va Khan Academy resurslariga murojaat qiling.",
         "Many universities no longer require the SAT essay, but some programs may still ask. If required, write a strong introduction, two or three key points, and a clear conclusion. Refer to College Board and Khan Academy guidelines.",
         "Многие университеты больше не требуют эссе SAT, но некоторые программы могут попросить. Если требуется, напишите сильное введение, два-три ключевых аргумента и четкое заключение. Обратитесь к рекомендациям College Board и Khan Academy."),

        ("SAT", "Registration",
         "SATga qanday ro'yxatdan o'tish kerak?", "How to register for the SAT?", "Как зарегистрироваться на SAT?",
         "SATga ro'yxatdan o'tish uchun collegeboard.org saytiga kirib, hisob yarating va test sanasini tanlang. To'lovni onlayn bajaring va tasdiqlovchi xatni saqlang. Ro'yxatdan o'tish haqida to'liq ma'lumotni College Board saytida topishingiz mumkin.",
         "To register for the SAT, go to collegeboard.org, create an account, and choose a test date. Pay online and save confirmation. Complete registration instructions are on the College Board site.",
         "Чтобы зарегистрироваться на SAT, зайдите на collegeboard.org, создайте учетную запись и выберите дату теста. Оплатите онлайн и сохраните подтверждение. Полные инструкции по регистрации есть на сайте College Board."),

        ("SAT", "Preparation",
         "SAT tayyorlanish rejasi qanday bo'lishi kerak?", "What should a SAT study plan look like?", "Как должен выглядеть план подготовки к SAT?",
         "O'zingiz uchun 10-12 haftalik reja tuzing: har hafta 3-4 mavzuni o'rganing, 1-2 rasmiy test ishlang va natijalarni tahlil qiling. Khan Academy, Magoosh va PrepScholar resurslari bilan muntazam mashq qiling. Vaqtni boshqarish va xatolarni qayta o'rganish asosiy omillar.",
         "Create a 10-12 week plan: study 3-4 topics weekly, complete 1-2 official tests, and analyze your results. Practice regularly with Khan Academy, Magoosh, and PrepScholar. Time management and reviewing mistakes are key.",
         "Составьте план на 10-12 недель: изучайте 3-4 темы в неделю, выполняйте 1-2 официальных теста и анализируйте результаты. Регулярно тренируйтесь с Khan Academy, Magoosh и PrepScholar. Управление временем и разбор ошибок — ключевые факторы."),

        # Universities Section
        ("UNIVERSITIES", "Requirements",
         "Top xalqaro universitetlarga kirish talablari qanday?", "What are the requirements for top universities?", "Каковы требования для топ-вузов?",
         "Top universitetlar uchun odatda yuqori ball, kuchli motivatsion xat, tavsiyanomalar va xalqaro til sertifikati kerak bo'ladi. AQShga kirish uchun SAT/ACT, Buyuk Britaniyaga uchun IELTS yoki TOEFL kerak bo'ladi. Resurslar: EducationUSA, UCAS va universitetlarning rasmiy saytlarini tekshiring.",
         "Top universities usually require high scores, a strong motivation letter, recommendation letters, and a language certificate. The US often needs SAT/ACT, the UK needs IELTS or TOEFL. Check EducationUSA, UCAS, and official university sites.",
         "Топ-вузам обычно нужны высокие баллы, сильное мотивационное письмо, рекомендации и языковой сертификат. В США часто требуется SAT/ACT, в Великобритании IELTS или TOEFL. Проверяйте EducationUSA, UCAS и официальные сайты университетов."),

        ("UNIVERSITIES", "Applications",
         "Universitetga qanday hujjatlar kerak?", "What documents are needed for university?", "Какие документы нужны для университета?",
         "Universitetga ariza, pasport, transkript, til sertifikati, motivatsion xat, tavsiyanoma va ba'zi hollarda moliyaviy dalillar talab qilinadi. UCAS, Common App va universitetlarning qabul sahifalarini diqqat bilan o'qing.",
         "Universities generally require an application, passport, transcript, language certificate, motivation letter, recommendation letters, and sometimes proof of funds. Read UCAS, Common App, and admission pages carefully.",
         "Университеты обычно требуют заявление, паспорт, выписку оценок, языковой сертификат, мотивационное письмо, рекомендации и иногда подтверждение средств. Внимательно читайте UCAS, Common App и страницы приёма."),

        ("UNIVERSITIES", "Scholarships",
         "Stipendiya qanday olish mumkin?", "How can I get a scholarship?", "Как получить стипендию?",
         "Stipendiyalar uchun yaxshi akademik natijalar, faol ijtimoiy hayot va mukammal ariza kerak. Resurslar: ScholarshipPortal, Studyportals, EducationUSA va universitetlarning stipendiya bo'limlari. Agar testlar talab qilinsa, IELTS va SAT ballarini oshiring.",
         "Scholarships require strong academics, extracurricular activities, and a complete application. Use ScholarshipPortal, Studyportals, EducationUSA, and university scholarship pages. Raise your IELTS and SAT scores if tests are required.",
         "Для стипендий нужны хорошие академические результаты, внеучебная активность и полная заявка. Используйте ScholarshipPortal, Studyportals, EducationUSA и страницы стипендий университетов. Улучшайте результаты IELTS и SAT, если тесты требуются."),

        ("UNIVERSITIES", "Visa",
         "Tashqi davlatga o'qishga ketish uchun qanday viza kerak?", "What visa is needed to study abroad?", "Какая виза нужна для учебы за границей?",
         "Talabalar vizasi uchun odatda universitetdan qabul xati, moliyaviy dalillar, sug'urta va pasport kerak bo'ladi. Elchixonaning rasmiy saytini va EducationUSA saytini tekshiring. Viza intervyusiga hujjatlaringizni tartib bilan tayyorlang.",
         "A student visa usually requires an admission letter, proof of funds, insurance, and passport. Check official embassy sites and EducationUSA. Prepare your documents neatly for the visa interview.",
         "Для студенческой визы обычно требуется письмо о приеме, подтверждение средств, страховка и паспорт. Проверяйте официальные сайты посольств и EducationUSA. Подготовьте документы аккуратно для визового интервью."),

        ("UNIVERSITIES", "Housing",
         "Talabalar uchun joy topishning eng yaxshi usuli nima?", "What is the best way to find student housing?", "Как лучше всего найти жилье для студентов?",
         "Turar joyni topish uchun avval kampus yotoqxonasini tekshiring, keyin Uniplaces, HousingAnywhere va Studyportals kabi saytlarni ko'rib chiqing. Narx, masofa, xavfsizlik va qo'shimcha xarajatlarni solishtiring. Universitet yotoqxonasi ko'pincha eng barqaror va xavfsiz variant hisoblanadi.",
         "First check campus accommodation, then review sites like Uniplaces, HousingAnywhere, and Studyportals. Compare cost, distance, safety, and extra fees. University housing is often more stable and secure.",
         "Сначала изучите кампусное жилье, затем просмотрите сайты Uniplaces, HousingAnywhere и Studyportals. Сравните цену, расстояние, безопасность и дополнительные расходы. Студенческое жилье часто более стабильное и безопасное."),

        ("UNIVERSITIES", "Resources",
         "Qayerdan universitetlar va grantlar haqida ma'lumot olish mumkin?", "Where can I find information about universities and grants?", "Где найти информацию о университетах и грантах?",
         "Universitetlar va grantlar haqida ma'lumotni EducationUSA, UCAS, Studyportals, ScholarshipPortal va uniagents.com saytlaridan topishingiz mumkin. Shuningdek, YouTube kanallari Mr. G, College Info Geek va StudyTube ham foydali. Har doim rasmiy saytlar va yangiliklar bo'limini tekshiring.",
         "Find university and grant information on EducationUSA, UCAS, Studyportals, ScholarshipPortal, and uniagents.com. YouTube channels like Mr. G, College Info Geek, and StudyTube are also helpful. Always verify details on official sites.",
         "Найдите информацию об университетах и грантах на EducationUSA, UCAS, Studyportals, ScholarshipPortal и uniagents.com. Полезны YouTube-каналы Mr. G, College Info Geek и StudyTube. Всегда проверяйте информацию на официальных сайтах."),

        ("IELTS", "Vocabulary",
         "IELTS uchun yangi so'zlarni qanday o'rganish kerak?", "How should I learn new vocabulary for IELTS?", "Как учить новые слова для IELTS?",
         "Yangi so'zlarni o'rganishda kontekst asosida mashq qiling: maqolalar, video va testlardan olingan iboralar bilan birga yozing. Quizlet, Memrise va Academic Word List kabi resurslar yordam beradi.",
         "Learn new words in context: write them with articles, videos, and test phrases. Use resources like Quizlet, Memrise, and Academic Word List.",
         "Учите новые слова в контексте: записывайте их с статьями, видео и фразами из тестов. Помогают ресурсы Quizlet, Memrise и Academic Word List."),

        ("IELTS", "Grammar",
         "IELTS imtihonida grammatika qanchalik muhim?", "How important is grammar in IELTS?", "Насколько важна грамматика в IELTS?",
         "Grammatika yozishda va gapirishda muhim. Grammatika xatolarini kamaytirishga e'tibor bering, ayniqsa Complex Sentence va Conditional tuzilmalarida. Grammarly, Cambridge Grammar va BBC Learning English sizga yordam beradi.",
         "Grammar is important in writing and speaking. Focus on reducing errors, especially in complex sentences and conditionals. Use Grammarly, Cambridge Grammar, and BBC Learning English.",
         "Грамматика важна в письме и говорении. Сосредоточьтесь на уменьшении ошибок, особенно в сложных предложениях и условных конструкциях. Помогут Grammarly, Cambridge Grammar и BBC Learning English."),

        ("SAT", "Reading Strategy",
         "SAT Reading bo'limida qanday savollarga obyektli javob berish kerak?", "How should I answer SAT Reading questions effectively?", "Как правильно отвечать на вопросы SAT Reading?",
         "Savollarga javob berishda matndagi so'zlarni izlang va biror tushuncha bilan taxmin qilmay yashirin ma'no topishga harakat qiling. Rasmiy College Board testlaridan foydalaning.",
         "When answering SAT Reading questions, look for words in the passage and avoid guessing. Use official College Board tests.",
         "При ответе на вопросы SAT Reading ищите слова в тексте и избегайте угадываний. Используйте официальные тесты College Board."),

        ("UNIVERSITIES", "Interview",
         "Universitet intervyusiga qanday tayyorlanish kerak?", "How should I prepare for a university interview?", "Как подготовиться к университетскому интервью?",
         "Intervyu uchun o'z ariza materiallaringizni, motivatsion xatingizni va ikkita kuchli javobni tayyorlang. Odatda motivatsion savollar, kelajak rejalar va o'zingiz haqingizdagi hikoya so'raladi.",
         "Prepare your application materials, personal statement, and two strong answers for a university interview. Expect questions about motivation, future plans, and your story.",
         "Подготовьте материалы заявки, мотивационное письмо и два сильных ответа для университетского интервью. Ожидайте вопросы о мотивации, планах на будущее и вашей истории."),
    ]

    for question in default_questions:
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

def add_user(user_id, lang, fullname, phone, location, email):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, lang, fullname, phone, location, email)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, lang, fullname, phone, location, email))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    conn.close()
    return res

def delete_user(user_id):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_questions_by_section(section):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question_uz, question_en, question_ru FROM QA_store WHERE section = ?", (section,))
    res = cursor.fetchall()
    conn.close()
    return res

def get_sections():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT section FROM QA_store ORDER BY section")
    res = [row[0] for row in cursor.fetchall()]
    conn.close()
    return res

def get_question_by_id(qa_id):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, section, category, question_uz, question_en, question_ru, answer_uz, answer_en, answer_ru FROM QA_store WHERE id = ?",
        (qa_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

def search_questions(query_text):
    conn = _get_connection()
    cursor = conn.cursor()
    like_term = f"%{query_text}%"
    cursor.execute(
        "SELECT id, section, category, question_uz, question_en, question_ru, answer_uz, answer_en, answer_ru "
        "FROM QA_store WHERE question_uz LIKE ? OR question_en LIKE ? OR question_ru LIKE ? "
        "OR answer_uz LIKE ? OR answer_en LIKE ? OR answer_ru LIKE ?",
        (like_term, like_term, like_term, like_term, like_term, like_term)
    )
    res = cursor.fetchall()
    conn.close()
    return res

def get_resources():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, section, category, question_uz, question_en, question_ru, answer_uz, answer_en, answer_ru "
        "FROM QA_store WHERE section = ? AND category = ?",
        ("UNIVERSITIES", "Resources")
    )
    res = cursor.fetchall()
    conn.close()
    return res

def find_question_by_text(section, text):
    conn = _get_connection()
    cursor = conn.cursor()
    like_term = f"%{text}%"
    cursor.execute(
        "SELECT id, question_uz, question_en, question_ru FROM QA_store WHERE section = ? AND (question_uz LIKE ? OR question_en LIKE ? OR question_ru LIKE ?)",
        (section, like_term, like_term, like_term)
    )
    res = cursor.fetchone()
    conn.close()
    return res

def get_answer_by_id(qa_id):
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT answer_uz, answer_en, answer_ru FROM QA_store WHERE id = ?", (qa_id,))
    res = cursor.fetchone()
    conn.close()
    return res