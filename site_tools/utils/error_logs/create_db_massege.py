from site_tools.models import ProcessesMessage


def create_message_db(message, notification=False):
    if not notification:
        message_db = f'Ошибка программы: {message}'
    else:
        message_db = f'Уведомление: {message}'
    ProcessesMessage.objects.create(message=message_db)
