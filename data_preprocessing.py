import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def augment_data(data):
    augmented_data = []
    for sentence in data:
        # Example augmentation: Reverse the sentence
        augmented_data.append(sentence[::-1])
    return augmented_data
