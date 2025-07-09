import sqlite3
import csv

DB_PATH = "data/crawled_articles.db"

def connect_db():
    return sqlite3.connect(DB_PATH)


def view_sample_entries(limit=10):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles")
    total = cursor.fetchone()[0]
    print(f"Total entries: {total}")

    cursor.execute("SELECT * FROM articles LIMIT ?", (limit,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


def clean_junk_links():
    conn = connect_db()
    cursor = conn.cursor()

    junk_patterns = [
        "%redirect%", "%login%", "%rss%", "%terms%",
        "%privacy%", "%portfolio%", "%editorial%",
        "%calendar%", "%watchlist%", "%contact%",
        "%glossary%", "%#%", "mailto:%", "javascript:%"
    ]

    deleted = 0
    for pattern in junk_patterns:
        cursor.execute("DELETE FROM articles WHERE url LIKE ?", (pattern,))
        deleted += cursor.rowcount

    conn.commit()
    conn.close()
    print(f"Removed {deleted} junk entries.")


def export_to_csv(output_file="cleaned_articles.csv"):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "title", "publish_date", "source"])
        writer.writerows(rows)

    conn.close()
    print(f"Exported {len(rows)} articles to {output_file}")


def reset_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS articles")
    cursor.execute("""
        CREATE TABLE articles (
            url TEXT PRIMARY KEY,
            title TEXT,
            publish_date TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database reset (clean slate).")
