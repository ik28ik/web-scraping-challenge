### Mission to Mars

This repo contains homework from the Web Scraping lecture series from The Columbia Engineering Data Analytics Boot Camp.

The purpose of this project is to demonstrate web scraping using Python and storing the scraped data in a non-relational database using MongoDB.

Using a jupyter notebook, initial web scraping is performed using the Python library Beautiful Soup. It scrapes data from five different websites to gather data related to the Mission to Mars and displays the information in a single HTML page.
The following information is displayed:
* The latest News, Title and Paragraph
* The current Featured Mars Image
* Mars weather tweet
* A table containing facts about the planet
* Obtained high resolution images for each of Mars's hemispheres

Using MongoDB with Flask was created a new HTML page that displays all of the information that was scraped from the URLs.

The Jupyter notebook was converted into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of the scraping code and return one Python dictionary containing all of the scraped data. The return value was stored in Mongo as a Python dictionary.

All the code for web scraping is copied into a python file to create a function to perform all the scraping at once. Using Pymongo in the function, the data is stored in a MongoDB database. This function is called into the app.py file. The app.py file is a flask app that is a single page app that allows the user to view all the scraped data. Once the app is opened, the user can view a Mars fact from NASA's twitter page, the weather on Mars, the featured Mars image on NASA's website, and images of every one of Mars' Hemispheres.

