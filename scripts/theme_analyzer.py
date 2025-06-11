from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import pandas as pd
import spacy 
import logging

logging.basicConfig(level=logging.INFO)

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """Tokenizes, removes stopwords, lemmatizes using spaCy."""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def get_top_keywords(row_vector, feature_names, top_n):
    row_array = row_vector.toarray().flatten()
    top_indices = row_array.argsort()[-top_n:][::-1]
    return [feature_names[i] for i in top_indices if row_array[i] > 0]

def extract_keywords(df: pd.DataFrame, text_column: str, top_n: int = 5) -> pd.DataFrame:
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(df[text_column])
    feature_names = vectorizer.get_feature_names_out()
    df['keywords'] = [get_top_keywords(tfidf_matrix[i], feature_names, top_n) for i in range(tfidf_matrix.shape[0])]
    logging.info("Extracted keywords using TF-IDF.")
    return df

def map_keywords_to_themes(keywords: list, theme_map: dict) -> list:
    themes = set()
    for kw in keywords:
        for key, theme in theme_map.items():
            if key in kw:
                themes.add(theme)
    return list(themes) if themes else ["Other"]

def aggregate_sentiment_by_rating(df: pd.DataFrame, bank_name: str) -> pd.DataFrame:
    agg = df.groupby('rating')['sentiment_score'].mean().reset_index()
    agg['bank'] = bank_name
    return agg

def get_examples_by_theme(df, theme_col='themes', text_col='review_text', max_examples=3):
    theme_examples = defaultdict(list)
    for _, row in df.iterrows():
        for theme in row[theme_col]:
            if len(theme_examples[theme]) < max_examples:
                theme_examples[theme].append(row[text_col])
    return theme_examples