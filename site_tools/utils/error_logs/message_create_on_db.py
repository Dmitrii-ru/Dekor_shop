class CatalogMassage:
    validate_message_error = {
        'pure': 'Не может быть пустым',
        '>max_length': 'Длинна должна быть меньше',
        'not_digit': 'Не возможно преобразовать в число',
        'not_unique': 'Уже существует -'
    }

    def __init__(self):
        pass
