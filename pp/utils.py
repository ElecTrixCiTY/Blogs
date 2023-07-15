import random
from django.conf import settings

def file_link(file_name):
    """
    Generates a link to the uploaded file.

    Args:
        file_name (str): The name of the uploaded file.

    Returns:
        str: The link to the uploaded file.
    """

    link_id = random.randint(100000, 999999)
    random.seed(file_name)
    url = settings.MEDIA_URL + 'uploaded'
    return f'{url}?link_id={link_id}'
