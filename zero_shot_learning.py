from transformers import pipeline

classifier = pipeline("zero-shot-classification")

def zero_shot_classification(text, labels):
    return classifier(text, labels)
