from crawler.crawler import NewsCrawler

sites = [
    "https://www.benzinga.com",
    "https://www.defenseworld.net",
    "https://www.insidermonkey.com",
    "https://www.fool.com",
    "https://www.marketbeat.com/headlines/"
]

if __name__ == "__main__":
    for site in sites:
        print(f"\n🕷️ Crawling: {site}")
        crawler = NewsCrawler(site)
        crawler.crawl()
