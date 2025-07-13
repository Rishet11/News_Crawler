# 📰 News Website Crawler

A Python-based crawler that scrapes new financial articles from 5 major news websites, extracts metadata (title, publish date), and stores them in a local SQLite database.

## Overview

This project automates the process of discovering and archiving the latest financial news articles. It scans supported websites, extracts relevant metadata, and ensures no duplicate articles are stored.

## Features
- URL deduplication to avoid duplicates
- Metadata extraction (title, publish date)
- Storage in a local SQLite database
- Easily extensible to support more websites

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rishet11/News_Crawler
   cd news_crawler
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start crawling and storing articles, run:
```bash
python main.py
```

## Configuration

- Edit the configuration section in `main.py` or the relevant config file to:
  - Add/remove target websites
  - Set crawling intervals
  - Adjust database settings

## Supported Websites

Currently supports scraping from the following financial news sources:
- [Benzinga](https://www.benzinga.com)
- [Defense World](https://www.defenseworld.net)
- [Insider Monkey](https://www.insidermonkey.com)
- [The Motley Fool](https://www.fool.com)
- [MarketBeat](https://www.marketbeat.com/headlines/)

## Database Schema

The SQLite database stores articles with the following fields:
- `url` (TEXT, Primary Key)
- `title` (TEXT)
- `publish_date` (TEXT)
- `source` (TEXT)


