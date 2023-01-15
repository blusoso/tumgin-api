import re


def create_slug(text: str):
    return re.sub('[^0-9a-zA-Z]+', '-', text).lower()
