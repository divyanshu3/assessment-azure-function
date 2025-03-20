from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
import logging, nltk

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
sia = SentimentIntensityAnalyzer()
language_code_mapping = {
    'ar': 'Arabic',
    'zh': 'Chinese',
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'hi': 'Hindi',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'la': 'Latin',
    'ne': 'Nepali',
    'fa': 'Persian',
    'pt': 'Portuguese',
    'ru': 'Russian'
}

# Sentiment Analysis
def analyse_sentiment(text):

    logging.info(f"sentiment analysis process started on text '{text}'")

    try:
        scores = sia.polarity_scores(text)
        compound = scores['compound']
        sentiment = 'Neutral'
        if compound > 0.5:
            sentiment = 'Positive'
        elif compound < -0.3:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        logging.info(f"sentiment analysis process successfully executed on text '{text}'")

        return sentiment, scores, 'request processed successfully', 200
    except Exception as e:

        logging.error(f"unable to perform sentiment anaylsis on text '{text}' due to error -> {str(e)}")
        return '','',f"some error occurred while proccessing the request. Error: {str(e)}", 501

# Language detection
def detect_text_language(text):

    try:
        text_language = language_code_mapping.get(detect(text))
        logging.info(f"language of the input text indentified successfully as '{text_language}'")

        return (text_language,"request processed successfully", 200) if text_language else ("", "unsupported language type passed. Please provide text in valid language.", 400)
    except Exception as e:

        logging.error(f'unable to indentified the language of the text due to error -> {str(e)}')
        return "unsupported language type passed. Please provide text in valid language.", 400
    

