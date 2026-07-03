SITE_CONTACT = {
    'owner': 'Юра',
    'location': 'Біла Церква, Київська обл.',
    'phone': '096 409 66 12',
    'phone_tel': '+380964096612',
    'email': 'pokrivlia.pid.kliuch@gmail.com',
}

SITE_STATS = {
    'projects': '400+',
    'experience': '20+',
    'warranty_years': '10',
}

SITE_HOURS = {
    'weekdays': 'Пн – Пт: 08:00 – 20:00',
    'weekend': 'Сб – Нд: 09:00 – 18:00',
}

CALLBACK_HINT = 'Відповімо протягом дня у робочий час'

MATERIAL_BRANDS = [
    'Ruukki',
    'Braas',
    'Velux',
    'Katepal',
    'BRYZA',
    'RAINWAY',
]

ROOF_MATERIALS = [
    ('metal_tile', 'Металочерепиця'),
    ('metal_profile', 'Металопрофіль'),
    ('bitumen_tile', 'Бітумна черепиця'),
    ('seam_roof', 'Фальцева покрівля'),
    ('ceramic_tile', 'Керамічна черепиця'),
]

WORK_TYPE_CHOICES = [
    ('new_roof', 'Монтаж нового даху'),
    ('recon_with_demolition', 'Реконструкція (з демонтажем старої покрівлі)'),
    ('recon_without_demolition', 'Реконструкція (без демонтажу)'),
]

AREA_CHOICES = [
    ('up_to_100', 'до 100 м²'),
    ('100_200', '100–200 м²'),
    ('200_300', '200–300 м²'),
    ('over_300', 'більше 300 м²'),
]

FLOORS_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('over_3', 'більше 3'),
]

MARQUEE_ITEMS = [
    'Монтаж покрівлі',
    'Реконструкція',
    'Гідроізоляція',
    'Утеплення',
    'Металочерепиця',
    'Металопрофіль',
    'Бітумна черепиця',
    'Фальцева покрівля',
    'Керамічна черепиця',
]

LOGO_PATH = 'images/logo.png'

HERO_HOME_URL = '/static/images/hero_roof_premium.png'

SERVICES_ITEMS = [
    {
        'icon': 'roofing',
        'variant': 'accent',
        'title': 'Монтаж покрівлі',
        'text': (
            'Повний цикл робіт від кроквяної системи до фінішного покриття '
            'металочерепицею, металопрофілем, бітумною або керамічною черепицею.'
        ),
        'features': [
            'Металочерепиця',
            'Металопрофіль',
            'Бітумна черепиця',
            'Фальцева покрівля',
            'Керамічна черепиця',
        ],
    },
    {
        'icon': 'construction',
        'variant': 'dark',
        'title': 'Реконструкція',
        'text': 'Оновлення застарілих покрівельних систем з покращенням енергоефективності та зовнішнього вигляду.',
        'features': ['Заміна покриття', 'Утеплення даху'],
    },
    {
        'icon': 'thermostat',
        'variant': 'accent',
        'title': 'Утеплення',
        'text': 'Енергоефективні рішення для теплоізоляції підпокрівельного простору та мансард.',
        'features': ['Мінеральна вата', 'Пінополістирол'],
    },
]

WHY_US_ITEMS = [
    {
        'num': '01',
        'title': 'Матеріали',
        'text': (
            'Якісні матеріали від європейських та українських виробників '
            'з гарантією від виробника.'
        ),
        'features': ['Керамічна черепиця', 'Фальцева покрівля', 'Бітумна черепиця'],
    },
    {
        'num': '02',
        'title': 'Інструменти',
        'text': 'Використовуємо інструмент від світових брендів та будівельні ліса.',
        'features': ['Milwaukee', 'Stihl', 'Makita', 'Dnipro-M', 'Будівельні ліса'],
    },
    {
        'num': '03',
        'title': 'Команда',
        'text': 'Бригади з досвідом понад 20 років, навчені на заводах-виробниках покрівель.',
        'features': ['Офіційний договір', 'Фіксована ціна', 'Виконання термінів'],
    },
]

ABOUT_FEATURES = [
    {
        'icon': 'verified',
        'title': 'Якісні матеріали',
        'text': 'Використання якісного матеріалу, перевіреного часом.',
    },
    {
        'icon': 'handyman',
        'title': 'Професійний інструмент',
        'text': 'Інструмент від відомих світових брендів.',
    },
    {
        'icon': 'architecture',
        'title': 'Технологія монтажу',
        'text': 'Дотримання технології покрівельних робіт.',
    },
    {
        'icon': 'schedule',
        'title': 'Терміни виконання',
        'text': 'Виконання монтажних робіт у визначений термін.',
    },
]

NAV_ITEMS = [
    {'key': 'home', 'label': 'Головна', 'url_name': 'core:home'},
    {'key': 'services', 'label': 'Послуги', 'url_name': 'core:services'},
    {'key': 'portfolio', 'label': 'Портфоліо', 'url_name': 'core:portfolio'},
    {'key': 'about', 'label': 'Про нас', 'url_name': 'core:about'},
    {'key': 'faq', 'label': 'Питання', 'url_name': 'core:contacts', 'anchor': 'faq'},
    {'key': 'contacts', 'label': 'Контакти', 'url_name': 'core:contacts', 'anchor': 'contacts'},
]

FAQ_ITEMS = [
    {
        'id': 1,
        'question': 'Як довго триває процес заміни покрівлі?',
        'answer': (
            'Термін залежить від площі та складності даху. Стандартний '
            'житловий будинок займає від 5 до 14 робочих днів. Ми надаємо '
            'детальний графік робіт одразу після підписання договору.'
        ),
    },
    {
        'id': 2,
        'question': 'Які матеріали ви використовуєте?',
        'answer': (
            'Ми працюємо з сертифікованими матеріалами європейських та '
            'українських брендів: Ruukki, Braas, Velux, Katepal, BRYZA, RAINWAY. '
            'Кожен матеріал має офіційну гарантію від виробника.'
        ),
    },
    {
        'id': 3,
        'question': 'Чи надаєте ви гарантію на роботи?',
        'answer': (
            'Так, ми надаємо офіційну гарантію на монтажні роботи до 10 років '
            'та гарантію на матеріали від виробника.'
        ),
    },
    {
        'id': 4,
        'question': 'Як розраховується вартість проекту?',
        'answer': (
            'Кошторис формується після безкоштовного виїзду для заміру даху. '
            'Ціна фіксується в договорі і не змінюється протягом виконання робіт.'
        ),
    },
]

PORTFOLIO_ITEMS = [
    {
        'id': 1,
        'title': 'Вілла Скандинавія',
        'category': 'metal',
        'date': 'Жовтень 2023',
        'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuACnzOywWOGtfsUflRdnWIOSn4nwudxyaDqSQnnO5JTK0z_K5c_Gpqf6cN9VuE601o_8jNAix_jOb7fUxKh5fChunTsiLGiAfsW9_S6LHoFcyLtTW4GVrf_1M0nI44mXljCS9SADu1F9fAVUj5yPITuSRR_nuRjbxxkrhaLBk4B7DiLKmJhK-fVfyO_i6v5Jq2UHCBWGj718HPUQ65PVk8oX77MuPCxxg2xK1tXXZ8Ud-0TKiEPBZw1YAMH8Q2f8p7OJU50wXV2-tAc',
        'alt': 'Сучасна вілла з цинковим дахом',
    },
    {
        'id': 2,
        'title': 'Чорна кераміка',
        'category': 'ceramic',
        'date': 'Серпень 2023',
        'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBgkkYZhttrx104m0_WNF4zbhxJgj5zPPmk7_cczF9050s1DOxqX-vl4Wj-ScNJP3pAa3uXSIyAZeHRd60pZJUbPjRePpqrdeQxWfg4l11FFWrSjBnacxmIuloLGgi2Scqpi7toZhIgsU5Q5DgnXc1_ec2yhmp2Mbucey4uOK-gbV1A_-m0DaL8rAJa03tIlyBPnbzppQxJH0DRzQ_zugKgvJU83hAmtEaN_BYf-E9CRgEYHI2a1jXVu1cNTtHBDytRWyjjppFHogI2',
        'alt': 'Деталі чорної керамічної черепиці',
    },
    {
        'id': 3,
        'title': 'Сонячний офіс',
        'category': 'commercial',
        'date': 'Червень 2023',
        'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBfZ_AKetEhA6f5NKEPZYDuDiP1wCDcHNZR-iIv-YWnTqa30LCPS1uTVNTQZb1b9qkQdGzPiZUIaF7uINK2NuLXkitkAqSHYHpmeqLXdYAYLjbV1HBcvN8G_6GlErVfqCgHzqkeai4kSK4g31VuIrwzknpgKXc3B2RsAVPoXME5p0NtlzsJk-vw8xJgmhZkysSbHLBPI8MlZMNxsF36UqPwtn15UoD7TWquBwHsRHCUehr49tkSfQXsysrtKIoErc-sj3QpR16g6RwR',
        'alt': 'Сучасний офіс з сонячними панелями',
    },
    {
        'id': 4,
        'title': 'Сланцевий мінімалізм',
        'category': 'slate',
        'date': 'Травень 2023',
        'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuC8u3vaYUv6ew2u95Q9EniGm6KvMc6ZWpEfCISGTZUQ5RmOMJMfvVYy6tvePa8CuatqzMAwVg02LQqnjfoZxREU1UcmL1xpSvItqyWX0d9xqYyk6ZJQv917-7QhS066-t1NvaghRhQQA6OORbqMYZrK3ntR94QQdqk2flXOJPxXsVqOhbPAwViRqlC_ETmnGsBV_W2OQgob6Rw2wKZRHJG_lHO7FrFhkiKwf5nOrf1nBLWmjt9epdjFgmpdtZEpiDjMGSsK5-hIZxYC',
        'alt': 'Мінімалістична сланцева покрівля',
    },
    {
        'id': 5,
        'title': 'Реставрація спадщини',
        'category': 'ceramic',
        'date': 'Березень 2023',
        'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCy9Tu23ZqywayYBdG1Tc1d50dJJtZMrqLAdVXgz7vtgk0scQ8inbBQGowhA8k2Cu35hk-GPdyCQOB_swaDm_Oy8w9ACh9cOTQxvWOL-YMRbzUXy3P8hmQxQnHrA0kShEnOQT36XQet7TGyNPdJpMKtkQeytW0hp4dWdOWvNy0dm-sCp4sXcCBzlV8QBmww2rEcxD9aF-bkRtgUNsaYJXjspYDDhGZf0rhbns5I_Znop7zzscLdcNC7Pkjw_VYJjl3rq74s9XXay1lC',
        'alt': 'Реставрація історичної покрівлі',
    },
    {
        'id': 6,
        'title': 'Промисловий комплекс',
        'category': 'commercial',
        'date': 'Січень 2023',
        'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAtrw_-iY-Lz66EAcHkdZloiwIMH5JiKHg0naK2DLnxtaJQqorrdsSNnpXlreXJcPwYG_hcEQpbjLkfmXnCpk_nH98TdMkfk-zWSv4qZt6gA1-cCtFSUDqXlXjADFfTHJEjHZuOGeXlj0eN1scS1tzdrOL8dq7axGOQgGFMpVgC_2VOcjxnkK96N3_-kvlH7M1b3-CoSXjM0SA5zLPjmzMzMiegITkLq0Zop84ijuos7Ier7Uia-h7elgPanh1ZKP2XTGsmRB3KiSjm',
        'alt': 'Промисловий покрівельний комплекс',
    },
]

PORTFOLIO_FILTERS = [
    {'slug': 'all', 'label': 'Усі проекти'},
    {'slug': 'metal', 'label': 'Метал'},
    {'slug': 'ceramic', 'label': 'Кераміка'},
    {'slug': 'slate', 'label': 'Сланець'},
    {'slug': 'commercial', 'label': 'Комерційні'},
]
