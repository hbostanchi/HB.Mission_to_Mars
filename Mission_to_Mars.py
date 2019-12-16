#!/usr/bin/env python
# coding: utf-8

# ### Featured Article
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd




# Mac users
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
# Visit the Quotes to Scrape site
url = 'http://quotes.toscrape.com/'
browser.visit(url)

# Parse the HTML
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
# Scrape the Title
title = soup.find('h2').text
title

# Scrape the top ten tags
tag_box = soup.find('div', class_='tags-box')
# tag_box
tags = tag_box.find_all('a', class_='tag')

for tag in tags:
    word = tag.text
    print(word)


url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# Chain .find onto our previously assigned variable, "slide_elem."
slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images
# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df
# Hemisphere Images
def hemispheres_image(browser):
    hemisphere={}
    hemisphere = []
    for i in range(0,4):
        url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        # Select link for each hemisphere
        image_link[i].click()
        #hTML parser set
        html = browser.html
        isoup_url = BeautifulSoup(html, 'html.parser')
        image_url = news_soup.select_one('img', class_='wide-image').get('src')
        # Find the links to see the full images and get titles
        image_link=browser.find_link_by_partial_text("Hemisphere Enhanced")[i]
        image_titles = isoup_url.find_all('h3')
        
        #hemisphere url
        hemisphere_url = f'https://astrogeology.usgs.gov{image_url}'

        # Store image url and title in dictionary hemi_dict
        hemisphere_dict = {
            'img_url': hemisphere_url,
            'title': image_titles[i].text
        }
        hemisphere.append(hemisphere_dict)
    browser.back()
    return hemisphere





