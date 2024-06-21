import os
import json
import feedparser
import requests
from bs4 import BeautifulSoup

def fetch_rss_feed(url):
    # Function to fetch and parse the RSS feed
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary,
        }

        response = requests.get(entry.link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_body = soup.find('body')  # Customize based on the actual website's structure
            article['content'] = article_body.get_text() if article_body else ''

        articles.append(article)

    return articles

def load_existing_articles(file_path):
    # Function to load existing articles from a JSON file
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_articles(file_path, articles):
    # Function to save articles to a JSON file
    with open(file_path, 'w') as file:
        json.dump(articles, file, indent=4)

def main():
    # Main function to fetch RSS feed and manage articles
    rss_url = 'https://podcastfeeds.nbcnews.com/RPWEjhKq'  
    file_path = 'articles.json'
    
    # Load existing articles
    existing_articles = load_existing_articles(file_path)
    existing_links = {article['link'] for article in existing_articles}
    
    # Fetch new articles
    new_articles = fetch_rss_feed(rss_url)
    
    # Filter out duplicates
    unique_articles = [article for article in new_articles if article['link'] not in existing_links]
    
    # Add unique new articles to existing ones
    all_articles = existing_articles + unique_articles
    
    # Save all articles back to the file
    save_articles(file_path, all_articles)
    
    # Print out the articles
    for article in unique_articles:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print(f"Published: {article['published']}")
        print(f"Summary: {article['summary']}")
        print(f"Content: {article['content']}")
        print('-' * 80)

if __name__ == "__main__":
    main()
