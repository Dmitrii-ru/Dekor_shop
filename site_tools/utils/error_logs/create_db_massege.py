from site_tools.models import ErrorMessage


def create_message_db(message):
    ErrorMessage.objects.create(message=message)
