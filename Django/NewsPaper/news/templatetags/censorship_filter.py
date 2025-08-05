import re

from django import template

register = template.Library()

CENSORSHIP_WORDS = [
    "fuck",
    "shit",
    "ass",
    "bitch",
    "bastard",
    "asshole",
    "dick",
    "cunt",
    "slut",
    "whore",
    "motherfucker",
    # для проверки
    'Model',
    'religious',
]


@register.filter(name='censor')
def censorship(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр 'censor' можно применять только к строкам")

    for word in CENSORSHIP_WORDS:
        pattern = rf"\b({word[0].lower()}|{word[0].upper()}){word[1:]}\b"

        def replace(match):
            word_match = match.group(0)
            # Оставляем первую букву, остальные заменяем на звёздочки
            return word_match[0] + "*" * (len(word_match) - 1)

        value = re.sub(pattern, replace, value)

    return value
