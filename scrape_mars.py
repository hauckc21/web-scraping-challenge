import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests

def init_browser():
    executable_path = {'executable_path': 'c:/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict = {}

    #Mars news site to scrape  
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

time.sleep(2)

html = browser.html
soup = bs(html, 'html.parser')

news_title = soup.find('div', class_='content_title').text
news_p = soup.find('div', class_='article_teaser_body').text

print(news_title)
print(news_p)


