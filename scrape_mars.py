# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import pandas as pd
import re

def scrape_info():

    # path
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser("chrome", **executable_path, headless=False)

    browser = Browser("chrome")

    # Visit the NASA news URL
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest '
    browser.visit(url)
    time.sleep(.2)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Create Mission to Mars global dictionary that can be imported into Mongo
    mars= {}

    # NASA MARS NEWS
    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find_all("div", class_="content_title")
    news_prgf = soup.find("div", class_="article_teaser_body").text

    print(news_title)
    print(news_prgf)

    # Dictionary entry from MARS NEWS
    mars['news_title']=news_title[1].text
    mars['news_p']=news_prgf

    # FEATURED IMAGE
    # Visit Mars Space Images 
    url2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(.02)

    # Click the image to view it
    click_image= browser.find_by_id('full_image')
    click_image.click()
    time.sleep(5)

    click_info=browser.find_link_by_partial_text('more info')
    click_info.click()
    time.sleep(5)

    # HTML Object and Parse with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve background-image url from figure tag 
    get_featured_image = soup.find("figure", class_="lede")

    # Retrieve image URL from src tag
    featured_image_url="https://www.jpl.nasa.gov"+get_featured_image.a.img["src"]

    # Display full link to featured image
    featured_image_url

    # Dictionary entry from MARS NEWS
    mars['featured_image_url']=featured_image_url 


    # Mars Weather 
    # Visit Weather Twitter through splinter module 
    url3='https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(2)

    # HTML Object and Parse with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain weather related words
    text_weather = re.compile(r'sol')
    mars_weather = soup.find('span', text = text_weather)
    mars_weather.text

    # Dictionary entry from WEATHER TWEET
    mars['weather'] = mars_weather.text


    # Mars Facts
    # Visit Mars facts url
    url="http://space-facts.com/mars/"

    # Use Pandas to "read_html" to parse the URL
    tables = pd.read_html(url)

    # Find Mars Facts DataFrame in the lists of DataFrames
    tables[0]
    df=tables[0]
    df

    # Assign the columns
    df.columns=['Attributes','Values']
    df
    html_table = df.to_html()
    html_table=html_table.replace('\n', '')

    # Dictionary entry from Mars Facts
    mars['facts'] = html_table
    df.to_html('table.html')


    # Mars Hemisphere
    # Visit hemispheres website through splinter module 
    url4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(.2)

    # HTML Object and Parse with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Retreive all items that contain mars hemispheres information
    links = browser.find_by_css('a.product-item h3')

    # Loop through the items previously stored
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[i].click()
        
        sample_element=browser.find_link_by_text('Sample').first
        hemisphere['image_url']=sample_element['href']
        hemisphere['title']=browser.find_by_css('h2.title').text

        hemisphere_image_urls.append(hemisphere)
        browser.back()
        
    # Dictionary entry from Mars Facts
    mars['hemisphere']= hemisphere_image_urls

    # Return mars_data dictionary 
    return mars

if __name__ == "__main__":
    print(scrape_info())   