cat > utils.py << 'EOF'
import re

def validate_phone(phone, lang='ua'):
    """
    Приймає номери з кодом і без.
    Якщо коду нема - додає по мові: UA=+380, PL=+48, RU=+380
    """
    # Прибираємо все крім цифр і +
    cleaned = re.sub(r'[^\d+]', '', phone.strip())
    
    # Якщо починається з + і має 10-15 цифр - ок
    if cleaned.startswith('+') and 11 <= len(cleaned) <= 16:
        return True, cleaned
    
    # Якщо тільки цифри
    if cleaned.isdigit():
        # Україна: 0XXXXXXXXX -> +380XXXXXXXXX
        if len(cleaned) == 10 and cleaned.startswith('0'):
            return True, '+38' + cleaned
        
        # Україна: 380XXXXXXXXX без +
        if len(cleaned) == 12 and cleaned.startswith('380'):
            return True, '+' + cleaned
        
        # Польща: 9 цифр без коду
        if len(cleaned) == 9 and lang == 'pl':
            return True, '+48' + cleaned
        
        # Польща: 48XXXXXXXXX без +
        if len(cleaned) == 11 and cleaned.startswith('48'):
            return True, '+' + cleaned
        
        # Якщо 9-10 цифр - додаємо код по мові
        if 9 <= len(cleaned) <= 10:
            if lang == 'pl':
                return True, '+48' + cleaned.lstrip('0')
            else:  # ua, ru
                return True, '+380' + cleaned.lstrip('0')
    
    return False, None

def format_phone_display(phone):
    """Для показу адміну красиво"""
    if phone.startswith('+380'):
        return phone.replace('+380', '0', 1)
    if phone.startswith('+48'):
        return phone
    return phone
EOF