import pymorphy2


def get_base_form_words(text):
    morph = pymorphy2.MorphAnalyzer()
    text = text.replace(':', ' ').replace(',', ' ').replace('"', ' ').replace("'", ' ')
    words = text.split()
    base_forms = []
    for word in words:
        parsed_word = morph.parse(word)[0]  # Получим первый разбор слова
        base_form = parsed_word.normal_form  # Получим базовую форму слова
        base_forms.append(base_form)
    search_vector_text = " ".join(base_forms)

    return search_vector_text

