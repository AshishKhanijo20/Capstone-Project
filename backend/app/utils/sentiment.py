import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the lexicon (only happens once)
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(text: str) -> str:
    """
    Analyzes text and returns 'positive', 'negative', or 'neutral'.
    """
    scores = analyzer.polarity_scores(text)
    # scores looks like: {'neg': 0.0, 'neu': 0.2, 'pos': 0.8, 'compound': 0.75}
    compound = scores['compound']

    if compound >= 0.05:
        return "positive"
    elif compound <= -0.02:
        return "negative"
    else:
        return "neutral"