import re

from django.utils.crypto import get_random_string

from files.models import file_upload


def test_file_upload_success():
    result = file_upload(None, f"{get_random_string()}.png")
    pattern = r"attachments\/[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}.png"
    assert re.match(pattern, result)
