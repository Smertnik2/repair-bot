# texts.py
LANGS = ['ua', 'ru', 'pl']

TEXTS = {
    'lang_select': {
        'ua': 'Оберіть мову',
        'ru': 'Выберите язык',
        'pl': 'Wybierz język'
    },
    'lang_ua': {'ua': '🇺🇦 Українська', 'ru': '🇺🇦 Украинский', 'pl': '🇺🇦 Ukraiński'},
    'lang_ru': {'ua': '🇷🇺 Російська', 'ru': '🇷🇺 Русский', 'pl': '🇷🇺 Rosyjski'},
    'lang_pl': {'ua': '🇵🇱 Польська', 'ru': '🇵🇱 Польский', 'pl': '🇵🇱 Polski'},
    'lang_set': {
        'ua': 'Мову змінено на українську ✅',
        'ru': 'Язык изменён на русский ✅',
        'pl': 'Język zmieniony na polski ✅'
    },
    'start_msg': {
        'ua': 'Привіт! Я бот сервісного центру. Допоможу оформити заявку на ремонт.',
        'ru': 'Привет! Я бот сервисного центра. Помогу оформить заявку на ремонт.',
        'pl': 'Cześć! Jestem botem serwisu. Pomogę Ci złożyć zgłoszenie naprawy.'
    },
    'menu_text': {
        'ua': 'Головне меню. Оберіть дію:',
        'ru': 'Главное меню. Выберите действие:',
        'pl': 'Menu główne. Wybierz akcję:'
    },
    'btn_new_order': {
        'ua': '🛠 Нова заявка',
        'ru': '🛠 Новая заявка',
        'pl': '🛠 Nowe zgłoszenie'
    },
    'btn_my_orders': {
        'ua': '📋 Мої заявки',
        'ru': '📋 Мои заявки',
        'pl': '📋 Moje zgłoszenia'
    },
    'btn_change_lang': {
        'ua': '🌐 Змінити мову',
        'ru': '🌐 Сменить язык',
        'pl': '🌐 Zmień język'
    },
    'choose_device': {
        'ua': 'Який пристрій ремонтуємо?',
        'ru': 'Какое устройство ремонтируем?',
        'pl': 'Jakie urządzenie naprawiamy?'
    },
    'btn_phone': {'ua': '📱 Телефон', 'ru': '📱 Телефон', 'pl': '📱 Telefon'},
    'btn_tablet': {'ua': '📱 Планшет', 'ru': '📱 Планшет', 'pl': '📱 Tablet'},
    'btn_laptop': {'ua': '💻 Ноутбук', 'ru': '💻 Ноутбук', 'pl': '💻 Laptop'},
    'btn_pc': {'ua': '🖥 ПК', 'ru': '🖥 ПК', 'pl': '🖥 Komputer'},
    'btn_console': {'ua': '🎮 Консоль', 'ru': '🎮 Консоль', 'pl': '🎮 Konsola'},
    'btn_other': {'ua': '🔧 Інше', 'ru': '🔧 Другое', 'pl': '🔧 Inne'},
    'ask_brand_model': {
        'ua': 'Вкажіть бренд та модель. Наприклад: iPhone 14 Pro',
        'ru': 'Укажите бренд и модель. Например: iPhone 14 Pro',
        'pl': 'Podaj markę i model. Np: iPhone 14 Pro'
    },
    'ask_problem': {
        'ua': 'Опишіть проблему з пристроєм',
        'ru': 'Опишите проблему с устройством',
        'pl': 'Opisz problem z urządzeniem'
    },
    'ask_phone': {
        'ua': 'Залиште ваш номер телефону для зв'язку. Формат: +48XXXXXXXXX',
        'ru': 'Оставьте ваш номер телефона для связи. Формат: +48XXXXXXXXX',
        'pl': 'Zostaw swój numer telefonu do kontaktu. Format: +48XXXXXXXXX'
    },
    'ask_name': {
        'ua': 'Як до вас звертатись?',
        'ru': 'Как к вам обращаться?',
        'pl': 'Jak się do Ciebie zwracać?'
    },
    'preview_title': {
        'ua': '🧾 Перевірте заявку',
        'ru': '🧾 Проверьте заявку',
        'pl': '🧾 Sprawdź zgłoszenie'
    },
    'preview_device': {
        'ua': '📱 Пристрій',
        'ru': '📱 Устройство',
        'pl': '📱 Urządzenie'
    },
    'preview_brand': {
        'ua': '🏷 Бренд/Модель',
        'ru': '🏷 Бренд/Модель',
        'pl': '🏷 Marka/Model'
    },
    'preview_problem': {
        'ua': '🔧 Проблема',
        'ru': '🔧 Проблема',
        'pl': '🔧 Problem'
    },
    'preview_phone': {
        'ua': '📞 Телефон',
        'ru': '📞 Телефон',
        'pl': '📞 Telefon'
    },
    'preview_name': {
        'ua': '👤 Ім'я',
        'ru': '👤 Имя',
        'pl': '👤 Imię'
    },
    'btn_confirm': {'ua': '✅ Відправити', 'ru': '✅ Отправить', 'pl': '✅ Wyślij'},
    'btn_edit': {'ua': '✏️ Змінити', 'ru': '✏️ Изменить', 'pl': '✏️ Edytuj'},
    'btn_cancel': {'ua': '❌ Скасувати', 'ru': '❌ Отмена', 'pl': '❌ Anuluj'},
    'btn_back': {'ua': '⬅️ Назад', 'ru': '⬅️ Назад', 'pl': '⬅️ Wstecz'},
    'order_sent': {
        'ua': 'Заявку #{id} відправлено! Ми зв'яжемось з вами найближчим часом.',
        'ru': 'Заявка #{id} отправлена! Мы свяжемся с вами в ближайшее время.',
        'pl': 'Zgłoszenie #{id} wysłane! Skontaktujemy się z Tobą wkrótce.'
    },
    'order_cancelled': {
        'ua': 'Заявку скасовано.',
        'ru': 'Заявка отменена.',
        'pl': 'Zgłoszenie anulowane.'
    },
    'error_phone': {
        'ua': 'Неправильний номер. Введіть у форматі +48XXXXXXXXX',
        'ru': 'Неправильный номер. Введите в формате +48XXXXXXXXX',
        'pl': 'Nieprawidłowy numer. Wpisz w formacie +48XXXXXXXXX'
    },
    'no_orders': {
        'ua': 'У вас поки немає заявок.',
        'ru': 'У вас пока нет заявок.',
        'pl': 'Nie masz jeszcze zgłoszeń.'
    },
    'your_orders': {
        'ua': '📋 Ваші заявки:',
        'ru': '📋 Ваши заявки:',
        'pl': '📋 Twoje zgłoszenia:'
    },
    'order_status_updated': {
        'ua': 'Статус заявки #{order_id} змінено на: {status}',
        'ru': 'Статус заявки #{order_id} изменён на: {status}',
        'pl': 'Status zgłoszenia #{order_id} zmieniony na: {status}'
    }
}

def t(lang, key, **kwargs):
    text = TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get('ru', key))
    return text.format(**kwargs)
