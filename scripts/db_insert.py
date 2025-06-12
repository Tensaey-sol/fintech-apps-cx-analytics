import oracledb
import pandas as pd
import os
import ast

def insert_reviews_into_oracle(user, password, dsn, input_dir="../data"):
    """
    Connects to Oracle DB and inserts bank and review data from CSVs.
    """
    try:
        # Connect to Oracle DB
        conn = oracledb.connect(user=user, password=password, dsn=dsn, mode=oracledb.SYSDBA)
        cursor = conn.cursor()

        # Load each bank's processed file
        files = [f for f in os.listdir(input_dir) if f.endswith("_with_sentiment_themes.csv")]

        bank_name_to_id = {}

        for file in files:
            df = pd.read_csv(os.path.join(input_dir, file))
            bank_name = df['bank_name'].iloc[0]

            # Insert bank if not already added
            if bank_name not in bank_name_to_id:
                bank_id_var = cursor.var(oracledb.NUMBER)
                cursor.execute("""
                    INSERT INTO banks (bank_name)
                    VALUES (:1)
                    RETURNING bank_id INTO :2
                """, (bank_name, bank_id_var))
                bank_id = bank_id_var.getvalue()[0]  # Extract the scalar value
                bank_name_to_id[bank_name] = bank_id

            bank_id = bank_name_to_id[bank_name]

            for idx, row in df.iterrows():
                try:
                    # Handle keywords
                    keywords = row['keywords']
                    if pd.isna(keywords):
                        keywords = ""
                    elif isinstance(keywords, str):
                        try:
                            # Try to parse as a stringified list
                            keywords_list = ast.literal_eval(keywords)
                            if isinstance(keywords_list, (list, tuple)):
                                keywords = ", ".join(str(k) for k in keywords_list)
                            else:
                                keywords = str(keywords_list)
                        except (ValueError, SyntaxError):
                            # If parsing fails, treat as a plain string
                            keywords = keywords
                    else:
                        # If not a string, convert to string
                        keywords = str(keywords)

                    # Handle themes
                    themes = row['themes']
                    if pd.isna(themes):
                        themes = ""
                    elif isinstance(themes, str):
                        try:
                            # Try to parse as a stringified list
                            themes_list = ast.literal_eval(themes)
                            if isinstance(themes_list, (list, tuple)):
                                themes = ", ".join(str(t) for t in themes_list)
                            else:
                                themes = str(themes_list)
                        except (ValueError, SyntaxError):
                            # If parsing fails, treat as a plain string
                            themes = themes
                    else:
                        # If not a string, convert to string
                        themes = str(themes)

                    # Execute INSERT statement
                    cursor.execute("""
                        INSERT INTO reviews (
                            bank_id, review_text, rating, review_date,
                            source, sentiment_label, sentiment_score, keywords, themes
                        ) VALUES (
                            :1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'),
                            :5, :6, :7, :8, :9
                        )
                    """, (
                        bank_id,
                        str(row.get('review_text', '')),
                        int(row.get('rating', 0)),
                        row.get('date'),
                        str(row.get('source', 'Google Play')),
                        str(row.get('sentiment_label', 'neutral')),
                        float(row.get('sentiment_score', 0.0)),
                        keywords,
                        themes
                    ))

                except Exception as e:
                    # Log the error and row data for debugging
                    print(f"Error inserting row {idx} in file {file}: {e}")
                    print(f"Row data: {row.to_dict()}")
                    raise  # Re-raise to stop execution and inspect the issue

        # Commit the transaction
        conn.commit()
        print("✅ All reviews and bank data inserted into Oracle successfully.")

    except Exception as e:
        # Roll back in case of error
        conn.rollback()
        raise e
    finally:
        # Clean up
        cursor.close()
        conn.close()