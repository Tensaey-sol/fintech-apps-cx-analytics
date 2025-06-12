import oracledb
from dotenv import load_dotenv
import os
from datetime import datetime
import pathlib

def generate_sql_dump(user, password, dsn, output_file="../SQL dump/database_dump.sql"):
    """
    Generate an SQL dump of the banks and reviews tables.
    """
    try:
        # Resolve the absolute path for output_file and ensure directory exists
        output_path = pathlib.Path(output_file).resolve()
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

        # Connect to Oracle DB
        conn = oracledb.connect(user=user, password=password, dsn=dsn, mode=oracledb.SYSDBA)
        cursor = conn.cursor()

        # Initialize SQL dump content
        sql_dump = []
        sql_dump.append(f"-- SQL Dump of banks and reviews tables")
        sql_dump.append(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sql_dump.append("")

        # Get DDL for tables using DBMS_METADATA
        tables = ["BANKS", "REVIEWS"]
        for table in tables:
            cursor.execute("""
                SELECT DBMS_METADATA.GET_DDL('TABLE', :table_name)
                FROM DUAL
            """, {"table_name": table})
            ddl = cursor.fetchone()[0].read()  # CLOB to string
            sql_dump.append(f"-- Table structure for {table.lower()}")
            sql_dump.append(ddl + ";")
            sql_dump.append("")

        # Get data from banks table
        sql_dump.append("-- Data for banks")
        cursor.execute("SELECT bank_id, bank_name FROM banks ORDER BY bank_id")
        rows = cursor.fetchall()
        for row in rows:
            bank_id, bank_name = row
            bank_name_escaped = bank_name.replace("'", "''")  # Escape single quotes
            sql_dump.append(
                f"INSERT INTO banks (bank_id, bank_name) VALUES ({bank_id}, '{bank_name_escaped}');"
            )
        sql_dump.append("")

        # Get data from reviews table
        sql_dump.append("-- Data for reviews")
        cursor.execute("""
            SELECT review_id, bank_id, review_text, rating, review_date,
                   source, sentiment_label, sentiment_score, keywords, themes
            FROM reviews
            ORDER BY review_id
        """)
        rows = cursor.fetchall()
        for row in rows:
            review_id, bank_id, review_text, rating, review_date, source, sentiment_label, sentiment_score, keywords, themes = row
            # Handle LOBs and NULLs with string escaping
            review_text_str = review_text.read() if isinstance(review_text, oracledb.LOB) else review_text
            review_text_escaped = "NULL" if review_text_str is None else f"'{review_text_str.replace("'", "''")}'"
            
            keywords_str = keywords.read() if isinstance(keywords, oracledb.LOB) else keywords
            keywords_escaped = "NULL" if keywords_str is None else f"'{keywords_str.replace("'", "''")}'"
            
            themes_str = themes.read() if isinstance(themes, oracledb.LOB) else themes
            themes_escaped = "NULL" if themes_str is None else f"'{themes_str.replace("'", "''")}'"
            
            source_escaped = "NULL" if source is None else f"'{source.replace("'", "''")}'"
            sentiment_label_escaped = "NULL" if sentiment_label is None else f"'{sentiment_label.replace("'", "''")}'"
            
            rating_val = "NULL" if rating is None else rating
            sentiment_score_val = "NULL" if sentiment_score is None else sentiment_score
            review_date_val = f"TO_DATE('{review_date.strftime('%Y-%m-%d')}', 'YYYY-MM-DD')" if review_date else "NULL"
            
            sql_dump.append(
                f"INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, "
                f"source, sentiment_label, sentiment_score, keywords, themes) "
                f"VALUES ({review_id}, {bank_id}, {review_text_escaped}, {rating_val}, {review_date_val}, "
                f"{source_escaped}, {sentiment_label_escaped}, {sentiment_score_val}, {keywords_escaped}, {themes_escaped});"
            )
        sql_dump.append("")

        # Add COMMIT statement
        sql_dump.append("COMMIT;")

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(sql_dump))
        
        print(f"\u2705 SQL dump written to {output_file}")

    except Exception as e:
        print(f"Error generating SQL dump: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_dotenv()
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    dsn = os.getenv("ORACLE_DSN")
    generate_sql_dump(user, password, dsn)