import pandas as pd

def clean_reviews(review_data: list) -> pd.DataFrame:
    """
    Clean and preprocess scraped reviews.

    Args:
        review_data (list): List of review dicts.

    Returns:
        pd.DataFrame: Cleaned review DataFrame.
    """
    df = pd.DataFrame(review_data)

    # Drop duplicates
    df.drop_duplicates(subset=['review_text', 'rating', 'date', 'bank_name'], inplace=True)

    # Drop rows with any nulls in key columns
    df.dropna(subset=['review_text', 'rating', 'date'], inplace=True)

    # Normalize column types
    df['rating'] = df['rating'].astype(int)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    return df