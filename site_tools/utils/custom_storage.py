from django.core.files.storage import FileSystemStorage
from django.core.files.storage import Storage
from core.settings import DOCUMENT_URL, DOCUMENT_ROOT


class DocumentStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = DOCUMENT_ROOT
        if base_url is None:
            base_url = DOCUMENT_URL
        super().__init__(location, base_url)
