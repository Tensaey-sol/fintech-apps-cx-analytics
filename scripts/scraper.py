from google_play_scraper import Sort, reviews
import logging

def scrape_reviews(app_id: str, bank_name: str, count: int = 500) -> list:
    """
    Scrape reviews from Google Play for a given app.
    
    Args:
        app_id (str): App ID on Google Play.
        bank_name (str): Human-readable bank name.
        count (int): Number of reviews to fetch.
    
    Returns:
        list: List of dicts with keys: review_text, rating, date, bank_name, source.
    """
    logging.info(f"Scraping reviews for {bank_name} ({app_id})")

    try:
        results, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count,
            filter_score_with=None
        )

        processed_reviews = []
        for entry in results:
            processed_reviews.append({
                'review_text': entry['content'],
                'rating': entry['score'],
                'date': entry['at'].strftime('%Y-%m-%d'),
                'bank_name': bank_name,
                'source': 'Google Play'
            })

        logging.info(f"Retrieved {len(processed_reviews)} reviews from {bank_name}")
        return processed_reviews

    except Exception as e:
        logging.error(f"Error scraping {bank_name}: {e}")
        return []