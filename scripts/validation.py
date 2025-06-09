import os
import pandas as pd

# Constants
EXPECTED_FILES = {
    "commercial_bank_of_ethiopia": "commercial_bank_of_ethiopia_reviews.csv",
    "bank_of_abyssinia": "bank_of_abyssinia_reviews.csv",
    "dashen_bank": "dashen_bank_reviews.csv"
}

REQUIRED_COLUMNS = ["review_text", "rating", "date", "bank_name", "source"]

def load_and_validate_reviews(data_dir):
    """
    Loads and validates bank review data from specific CSV files.
    
    Args:
        data_dir (str): Path to directory containing bank review CSVs
        
    Returns:
        dict: {
            'combined_df': Combined DataFrame of all reviews,
            'summary_df': DataFrame with per-file stats,
            'missing_files': List of missing expected files,
            'metrics': Dictionary of overall metrics
        }
    """
    all_data = []
    summary = []
    missing_files = []
    
    # Check for expected files
    for bank_name, expected_fname in EXPECTED_FILES.items():
        file_path = os.path.join(data_dir, expected_fname)
        
        if not os.path.exists(file_path):
            missing_files.append(expected_fname)
            continue
            
        df = pd.read_csv(file_path)
        
        # Validate columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns in {expected_fname}: {', '.join(missing_cols)}")
        
        # Calculate metrics
        total = len(df)
        missing = df[REQUIRED_COLUMNS].isnull().sum().sum()
        missing_pct = (missing / (total * len(REQUIRED_COLUMNS))) * 100
        
        duplicates = df.duplicated(subset=["review_text", "rating", "date", "bank_name"]).sum()
        date_format_ok = df["date"].str.match(r"\d{4}-\d{2}-\d{2}").all()
        
        all_data.append(df)
        
        summary.append({
            "bank": bank_name.replace("_", " ").title(),
            "file": expected_fname,
            "reviews": total,
            "missing_values": missing,
            "missing_%": round(missing_pct, 2),
            "duplicates": duplicates,
            "date_format_OK": date_format_ok
        })

    # Combine all data
    combined = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    summary_df = pd.DataFrame(summary)
    
    # Calculate overall metrics
    metrics = {}
    if not combined.empty:
        total_reviews = len(combined)
        overall_missing = combined[REQUIRED_COLUMNS].isnull().sum().sum()
        overall_pct = (overall_missing / (total_reviews * len(REQUIRED_COLUMNS))) * 100
        total_duplicates = summary_df["duplicates"].sum()
        
        metrics = {
            'total_reviews': total_reviews,
            'overall_missing_pct': round(overall_pct, 2),
            'total_duplicates': total_duplicates,
            'all_files_present': len(missing_files) == 0
        }
    
    return {
        'combined_df': combined,
        'summary_df': summary_df,
        'missing_files': missing_files,
        'metrics': metrics
    }