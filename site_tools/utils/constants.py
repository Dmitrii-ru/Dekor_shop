const_columns = {
    'Номенклатура',
    "Наименование полное",
    'Розничная цена',
    'Ед. изм.',
    'Остаток на складе',
    'Номенклатура.Код'
}

status_catalog_dict = {
    1: "Жду каталог",
    2: "Идет загрузка каталога",
    3: "Возникла ошибка при предварительной обработке каталога",
    4: "Возникла ошибка при взаимодействие с данными с на сайте",
    5: "Возникла ошибка при подготовке отчета",
    6: "Каталог сайта успешно обновлен",
    7: "Загрузка каталога для предварительного просмотра прошла успешно, за исключением не уникальных позиций",
    8: 'Каталог не найден',
    9: 'Идет загрузка каталога на сайт'
}

report_columns_dict = {
    'new': "Новые позиции",  # 4
    'recomm_promotion': 'Рекомендованное позиции для акции',  # 3
    'promotion_false': 'Исключены из акции',  # 2
    'is_actual_true': 'Возврат из архива',  # 1
    'is_actual_false': "В архив",  # 5
}

report_message = {
    1: 'Возврат из архива',
    2: 'Исключен из акции',
    3: 'Рекомендован к акции',
    4: 'Новая позиция',
    5: 'Переведен в архив'
}

validate_upload_catalog = {
    'pure': 'Не может быть пустым',
    '>max_length': 'Длинна должна быть меньше',
    'not_digit': 'Не возможно преобразовать в число',
    'not_unique': 'Уже существует -',
    'slug':'Невозможно создать слаг'
}


def create_status_catalog(num, massage=None):
    if massage:
        return f'{status_catalog_dict[num]}: {massage}'
    else:
        return status_catalog_dict[num]


stop_list_product = ['*', 'яя*', 'яя', 'XXX', ]
