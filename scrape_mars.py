# Dependencies
from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time
import pandas as pd

def scrape_info():

    # path
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=False)

    # Visit the NASA news URL
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest '
    browser.visit(url)
    time.sleep(.2)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars= {}

    news = soup.find("div", class_="list_text")
    news_title = news.find("div", class_="content_title").text
    news_prgf = news.find("div", class_="article_teaser_body").text

    print(news_title)
    print(news_prgf)

    mars['news_title']=news_title
    mars['news_p']=news_prgf

    url2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(.02)

    click_image= browser.find_by_id('full_image')
    click_image.click()
    time.sleep(5)

    click_info=browser.find_link_by_partial_text('more info')
    click_info.click()
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    get_featured_image = soup.find("figure", class_="lede")

    featured_image_url="https://www.jpl.nasa.gov"+get_featured_image.a.img["src"]

    featured_image_url

    mars['featured_image_url']=featured_image_url 

    # url3='https://twitter.com/marswxreport?lang=en'
    # browser.visit(url3)
    # time.sleep(.2)

    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')

    # results = soup2.find_all('div', class_="js-tweet-text-container")
    #     results
    #     mars_weather=[]
    #     for result in results:
    #         mars_weather.append(result.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text)
    #     #print(mars_weather)
    #     #print("<---------------------------------------------------------------------------------->")
    #     mars["weather"] = mars_weather[0]

    df=pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=['decription']
    # df.set_index('decription', inplace=True)
    html_table=df.to_html
    mars['facts']=html_table

    url4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(.2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item h3')
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[i].click()
        
        sample_element=browser.find_link_by_text('Sample').first
        hemisphere['image_url']=sample_element['href']
        hemisphere['title']=browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    mars['hemisphere']= hemisphere_image_urls

    return mars

if __name__ == "__main__":
    print(scrape_info())   