def clean_text(text):
    text = text.lower()
    text = " ".join(text.split())
    return text