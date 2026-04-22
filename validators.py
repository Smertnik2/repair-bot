import re

# Україна: +380XXXXXXXXX, 380XXXXXXXXX, 0XXXXXXXXX - 9 цифр після коду
# Польща: +48XXXXXXXXX, 48XXXXXXXXX - 9 цифр після коду

UA_PATTERNS = [
    r'^\+380\d{9}$',  # +380991234567
    r'^380\d{9}$',    # 380991234567
    r'^0\d{9}$',      # 0991234567
]

PL_PATTERNS = [
    r'^\+48\d{9}$',   # +48123456789
    r'^48\d{9}$',     # 48123456789
]

def validate_phone(phone):
    """Перевіряє телефон UA/PL. Повертає (is_valid, normalized_phone, country)"""
    # Чистимо пробіли, дефіси, дужки
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Україна
    for pattern in UA_PATTERNS:
        if re.match(pattern, cleaned):
            # Нормалізуємо до +380XXXXXXXXX
            if cleaned.startswith('0'):
                normalized = '+38' + cleaned
            elif cleaned.startswith('380'):
                normalized = '+' + cleaned
            else:
                normalized = cleaned
            return True, normalized, 'UA'
    
    # Польща
    for pattern in PL_PATTERNS:
        if re.match(pattern, cleaned):
            # Нормалізуємо до +48XXXXXXXXX
            if cleaned.startswith('48'):
                normalized = '+' + cleaned
            else:
                normalized = cleaned
            return True, normalized, 'PL'
    
    return False, phone, None

def format_phone_error(lang='ua'):
    if lang == 'ua':
        return '❌ Невірний формат номера\n\nДопустимі формати:\n🇺🇦 Україна: +380991234567 або 0991234567\n🇵🇱 Польща: +48123456789\n\nВведи номер ще раз:'
    else:
        return '❌ Invalid phone format\n\nAllowed:\n🇺🇦 Ukraine: +380991234567 or 0991234567\n🇵🇱 Poland: +48123456789\n\nEnter again:'