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

    #Mars image scrape
    jpl_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    image_soup = bs(html, 'html.parser')

    #Feature Image Link
    path = image_soup.find_all('img')[3]['src']
    featured_image_url = jpl_url + path

    #Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    #get tables
    facts_df = pd.read_html(facts_url)[0]
    facts_df

    #convert to an html table
    facts_html = facts_df.to_html(index=False, header=False)
    facts_html