import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from urllib.parse import urlparse, urljoin  


class NewsCrawler:
    def __init__(self, base_url, db_path="data/crawled_articles.db"):
        self.base_url = base_url
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                title TEXT,
                publish_date TEXT,
                source TEXT
            )
        ''')
        self.conn.commit()

    def has_been_crawled(self, url):
        self.cursor.execute("SELECT 1 FROM articles WHERE url=?", (url,))
        return self.cursor.fetchone() is not None

    def save_article(self, url, title, publish_date, source):
        self.cursor.execute(
            "INSERT OR IGNORE INTO articles (url, title, publish_date, source) VALUES (?, ?, ?, ?)",
            (url, title, publish_date, source)
        )
        self.conn.commit()


    def extract_links(self, soup):
        raw_links = [a['href'] for a in soup.find_all('a', href=True)]
        filtered = []

        for link in raw_links:
            if not link:
                continue

            # Skip javascript, mailto, anchors, or social media
            if link.startswith("javascript:") or link.startswith("mailto:") or link.strip() in ["#", "/"]:
                continue
            if any(social in link for social in ["tiktok.com", "instagram.com", "youtube.com", "facebook.com", "linkedin.com"]):
                continue

            full_url = urljoin(self.base_url, link)
            

            # non-http/http links
            if urlparse(full_url).scheme not in ("http", "https"):
                continue

            if any(bad in full_url.lower() for bad in [
            "tiktok", "instagram", "youtube", "facebook", "linkedin",
            "/login", "/register", "/contact", "/about", "/terms", "/privacy",
            "/sitemap", "/glossary", "/dictionary", "/disclaimer", "/rss",
            "/watchlist", "/subscribe", "/portfolio", "/calculator"
            ]):
                continue
            
            
            filtered.append(full_url)

        return list(set(filtered))


    def extract_metadata(self, article_url):
        try:
            res = requests.get(article_url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.title.text.strip() if soup.title else "No Title"
            date_tag = soup.find('time')
            publish_date = date_tag.text.strip() if date_tag else "Unknown"
            return title, publish_date
        except Exception as e:
            print(f"[ERROR] Failed to parse {article_url}: {e}")
            return None, None

    def crawl(self):
        try:
            res = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            article_links = self.extract_links(soup)

            print(f"[INFO] Found {len(article_links)} links on {self.base_url}")
 
            bad_title_keywords = [
                "login", "register", "privacy", "terms", "editorial",
                "portfolio", "email protection", "access denied", "cloudflare",
                "rss", "contact", "guidelines", "interstitial", "subscribe",
                "home", "dictionary", "watchlist", "about", "glossary", "calendar",
                "calculator", "disclaimer", "legal", "tools", "data", "products",
                "news", "report", "newsletter", "media", "status", "account",
                "market data", "api", "research", "app store", "cookie", "%doc_title%"
            ]


            for link in article_links:
                full_url = urljoin(self.base_url, link)
                full_url = full_url.split("?")[0]  

                if not self.has_been_crawled(full_url):
                    title, pub_date = self.extract_metadata(full_url)

                    # Filter titles
                    if title and title.strip().lower() not in ["", "no title"]:
                        if title and not any(bad in title.lower() for bad in bad_title_keywords):
                            self.save_article(full_url, title, pub_date, self.base_url)
                            print(f"[SAVED] {title}")
                        else:
                            print(f"[SKIPPED] {title}")
                        
                        time.sleep(1)



        except Exception as e:
            print(f"[CRASH] Failed to crawl {self.base_url}: {e}")
