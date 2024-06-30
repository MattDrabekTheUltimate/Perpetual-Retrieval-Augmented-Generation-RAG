from transformers import pipeline

# Initialize NLP pipelines
ner_pipeline = pipeline("ner")
sentiment_pipeline = pipeline("sentiment-analysis")
syntax_pipeline = pipeline("syntax")

def process_query(query):
    ner_results = ner_pipeline(query)
    sentiment_results = sentiment_pipeline(query)
    syntax_results = syntax_pipeline(query)

    # Process and utilize these results for better query understanding
    return ner_results, sentiment_results, syntax_results
