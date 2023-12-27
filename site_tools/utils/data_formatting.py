import re

list_of_misspelled_words = {
    'Разночвет': 'Разноцвет',
    'pro, fflex': 'Profflex',
    'техно, николь': 'Технониколь',
}

# в конце не отображать эти надписи
stop_desp = [
    'XXX', 'яя'
]


def process_inside_brackets(match):
    new_text = []
    text_inside_brackets = match.group(1)
    for word in text_inside_brackets.split(','):
        word = re.sub(r'([a-zа-я])([A-ZА-Я])', r'\1 \2', word)
        new_text.append(word.strip())
    return f'({", ".join(new_text).capitalize()})'


def inside_brackets(match):
    processed_text = re.sub(r'\((.*?)\)', lambda x: process_inside_brackets(x), match.group(0))
    return processed_text


def check_brackets(text):
    if text.count('(') > text.count(')'):
        text += ')'
    return text


def capitalize_inside_quotes(text):
    matchs = list(re.finditer(r'"([^"]+)"', text))
    for match in matchs:
        text_in_quotes = match.group(1)
        capitalized_text = text_in_quotes.capitalize()
        text = text.replace(match.group(0), f'"{capitalized_text}"')
    return text


def capitalize_latin_words(match):
    word = match.group(0)
    return word.capitalize()


def replace_space(text):
    # text = text.replace('.', '. ').replace(',', ', ').replace(' .', '. ').replace(' ,', ', ')
    text = text.strip()
    return re.sub(r'\s+', ' ', text)


def break_title_in_words(text):
    return re.sub(r'([a-zа-я])([A-ZА-Я])', r'\1, \2', text)


def format_vector_search(text):
    text = text.replace(':', ' ').replace(',', ' ').replace('"', ' ').replace("'", ' ')
    return text


def transform_site_name(text):
    text = break_title_in_words(text)
    text = re.sub(r'\b[a-zA-Z]+\b', capitalize_latin_words, text)
    text = re.sub(r'\((.*?)\)', inside_brackets, check_brackets(text))
    text = text.replace(':', ' ').replace(';', ' ').replace(',', ', ')
    text = capitalize_inside_quotes(text)
    text = replace_space(text)
    return text
