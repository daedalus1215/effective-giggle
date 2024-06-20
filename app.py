import feedparser
import requests
from bs4 import BeautifulSoup


def fetch_rss_feed(url):
    # Parse the RSS feed
    feed = feedparser.parse(url)
    articles = []
    
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary,
        }
        
        # Fetch the article content
        # response = requests.get(entry.link)
        # if response.status_code == 200:
        #     soup = BeautifulSoup(response.content, 'html.parser')
        #     article_body = soup.find('body')  # This needs to be customized based on the actual website's structure
        #     article['content'] = article_body.get_text() if article_body else ''
        
        articles.append(article)
    
    return articles


print(fetch_rss_feed("rss.xml"))