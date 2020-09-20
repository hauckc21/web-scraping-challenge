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
    #wait for page to load
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    #retrieve most recent news title and paragraph
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text


    #Mars image scrape
    jpl_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    #wait for page to load
    time.sleep(2)
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


    
    # Mars hemispheres to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    hemispheres_html = browser.html

    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    #Mars hemisphere data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    # Iterate through each hemisphere
    for sphere in mars_hemispheres:
        
        # Collect Title
        hemisphere = sphere.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Collect image link by browsing to page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
        
        time.sleep(2)
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        
        hemisphere_image_urls.append(image_dict))


    #create mars dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(facts_html),
        "hemisphere_images": hemisphere_image_urls
    }

    #close browser session
    browser.quit()
    
    return mars_dict