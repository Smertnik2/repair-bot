def t(lang, key, **kwargs):
    texts = {
        'ua': {
            'bot_stopped': '🛑 Бот зупинено. Напишіть /start для перезапуску.',
            'history_cleared': '🗑️ Історію очищено.',
            'lang_changed': '✅ Мову змінено на українську.',
            'choose_again': '👇 Оберіть пристрій з меню.',
            'my_orders': '📋 Мої замовлення',
            'no_orders': '📭 У вас ще немає замовлень.',
            'your_orders': '📋 Ваші замовлення ({count}):\n\n',
            'order_status': '📊 Статус: {status}\n',
            'order_discount': '💰 Знижка: {discount}%\n',
            'order_date': '📅 Дата: {created}',
            'service_type': '🔧 Оберіть тип сервісу:',
            'service_center': '🏢 В сервіс',
            'service_home': '🚗 Виїзд майстра',
            'selected_device': '✅ Обрано: {device}\n📝 Опишіть проблему, додайте фото. Коли готові — напишіть "готово".',
            'add_details': '📝 Додайте опис проблеми або фото.',
            'almost_done': '📱 Майже готово. Надішліть ваш номер телефону.',
            'saved': '💾 Збережено.',
            'phone_invalid': '❌ Номер телефону некоректний. Введіть мінімум 10 цифр.',
            'ask_address': '📍 Вкажіть адресу для виїзду майстра.',
            'order_accepted': '✅ Замовлення #{order_id} прийнято!\n',
            'your_discount': '💰 Ваша знижка: {discount}%\n',
            'your_ref': '🎁 Ваш реферальний код: {ref_code}\nПоділіться з друзями.\n',
            'master_contact': '👨‍🔧 Майстер зв\'яжеться з вами найближчим часом.',
            'order_status_updated': '🔄 Статус замовлення #{order_id} змінено на: {status}',
            'not_understand': '❓ Не зрозумів. Оберіть дію з меню.'
        },
        'ru': {
            'bot_stopped': '🛑 Бот остановлен. Напишите /start для перезапуска.',
            'history_cleared': '🗑️ История очищена.',
            'lang_changed': '✅ Язык изменен на русский.',
            'choose_again': '👇 Выберите устройство из меню.',
            'my_orders': '📋 Мои заказы',
            'no_orders': '📭 У вас еще нет заказов.',
            'your_orders': '📋 Ваши заказы ({count}):\n\n',
            'order_status': '📊 Статус: {status}\n',
            'order_discount': '💰 Скидка: {discount}%\n',
            'order_date': '📅 Дата: {created}',
            'service_type': '🔧 Выберите тип сервиса:',
            'service_center': '🏢 В сервис',
            'service_home': '🚗 Выезд мастера',
            'selected_device': '✅ Выбрано: {device}\n📝 Опишите проблему, добавьте фото. Когда готовы — напишите "готово".',
            'add_details': '📝 Добавьте описание проблемы или фото.',
            'almost_done': '📱 Почти готово. Отправьте ваш номер телефона.',
            'saved': '💾 Сохранено.',
            'phone_invalid': '❌ Номер телефона некорректен. Введите минимум 10 цифр.',
            'ask_address': '📍 Укажите адрес для выезда мастера.',
            'order_accepted': '✅ Заказ #{order_id} принят!\n',
            'your_discount': '💰 Ваша скидка: {discount}%\n',
            'your_ref': '🎁 Ваш реферальный код: {ref_code}\nПоделитесь с друзьями.\n',
            'master_contact': '👨‍🔧 Мастер свяжется с вами в ближайшее время.',
            'order_status_updated': '🔄 Статус заказа #{order_id} изменен на: {status}',
            'not_understand': '❓ Не понял. Выберите действие из меню.'
        },
        'pl': {
            'bot_stopped': '🛑 Bot zatrzymany. Napisz /start aby zrestartować.',
            'history_cleared': '🗑️ Historia wyczyszczona.',
            'lang_changed': '✅ Język zmieniony na polski.',
            'choose_again': '👇 Wybierz urządzenie z menu.',
            'my_orders': '📋 Moje zamówienia',
            'no_orders': '📭 Nie masz jeszcze zamówień.',
            'your_orders': '📋 Twoje zamówienia ({count}):\n\n',
            'order_status': '📊 Status: {status}\n',
            'order_discount': '💰 Zniżka: {discount}%\n',
            'order_date': '📅 Data: {created}',
            'service_type': '🔧 Wybierz typ serwisu:',
            'service_center': '🏢 Do serwisu',
            'service_home': '🚗 Wyjazd mistrza',
            'selected_device': '✅ Wybrano: {device}\n📝 Opisz problem, dodaj zdjęcie. Gdy gotowe — napisz "gotowe".',
            'add_details': '📝 Dodaj opis problemu lub zdjęcie.',
            'almost_done': '📱 Prawie gotowe. Wyślij swój numer telefonu.',
            'saved': '💾 Zapisano.',
            'phone_invalid': '❌ Numer telefonu nieprawidłowy. Wprowadź minimum 10 cyfr.',
            'ask_address': '📍 Podaj adres dla wyjazdu mistrza.',
            'order_accepted': '✅ Zamówienie #{order_id} przyjęte!\n',
            'your_discount': '💰 Twoja zniżka: {discount}%\n',
            'your_ref': '🎁 Twój kod polecający: {ref_code}\nPodziel się z przyjaciółmi.\n',
            'master_contact': '👨‍🔧 Mistrz skontaktuje się z Tobą wkrótce.',
            'order_status_updated': '🔄 Status zamówienia #{order_id} zmieniony na: {status}',
            'not_understand': '❓ Nie rozumiem. Wybierz akcję z menu.'
        }
    }
    return texts.get(lang, texts['ua']).get(key, key).format(**kwargs)

MENU_ITEMS = {
    'PHONE': {'ua': '📱 Телефон', 'ru': '📱 Телефон', 'pl': '📱 Telefon'},
    'LAPTOP': {'ua': '💻 Ноутбук', 'ru': '💻 Ноутбук', 'pl': '💻 Laptop'},
    'PC': {'ua': '🖥️ Комп\'ютер', 'ru': '🖥️ Компьютер', 'pl': '🖥️ Komputer'},
    'TABLET': {'ua': '📲 Планшет', 'ru': '📲 Планшет', 'pl': '📲 Tablet'}
}

LANG_COMMANDS = ['/lang', '/language', 'мова', 'язык', 'język']

STATUS_TRANS = {
    'Нове': {'ua': '🆕 Нове', 'ru': '🆕 Новое', 'pl': '🆕 Nowe'},
    'В роботі': {'ua': '⚙️ В роботі', 'ru': '⚙️ В работе', 'pl': '⚙️ W trakcie'},
    'Готово': {'ua': '✅ Готово', 'ru': '✅ Готово', 'pl': '✅ Gotowe'},
    'Скасовано': {'ua': '❌ Скасовано', 'ru': '❌ Отменено', 'pl': '❌ Anulowano'}
}