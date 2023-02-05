import re


def preprocessing(text):
    text = text.lower()
    text = re.sub(r'([a-z])\.([a-z])', r'\1. \2', text)
    return text