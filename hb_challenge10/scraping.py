#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup# In[4]:
def mars_news(browser):


    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):


    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # In[10]:


    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()


    # In[11]:



    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()


    # In[12]:


    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')


    # In[13]:


    # Find the relative image url
    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # In[14]:


    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():

    import pandas as pd  
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    return df.to_html()

def hemispheres_image(browser):
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemispheres = []
    for i in range(0,4):
        image_link=browser.find_link_by_partial_text("Hemisphere Enhanced")[i]
        image_link.click()
        html = browser.html
        #hemisphere url
        isoup_url = BeautifulSoup(html, 'html.parser')
        #image_url = isoup_url.select_one('img.wide-image').get("src")
        
    
        hemisphere_src = isoup_url.find('img', class_='wide-image')['src']   
        hemisphere_url= f'https://astrogeology.usgs.gov{hemisphere_src}'
        print(hemisphere_url)
        
        #hemisphere title
        hemisphere_title = (isoup_url.find('h2', class_='title')).text
        print(hemisphere_title)
        
        #store in list
        hemispheres.append({
            "img_url": hemisphere_url,
            "title": hemisphere_title
        })
        print(hemispheres)
        
        #go back in browser
        browser.back()
    return hemispheres



def scrape_all():
    import datetime as dt
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres_image": hemispheres_image(browser),
        "last_modified": dt.datetime.now()
    }
    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())