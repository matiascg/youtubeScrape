import requests
from bs4 import BeautifulSoup as soup
import youtube_dl
from selenium import webdriver

#Setup
driver = webdriver.Chrome()
driver.get('https://www.youtube.com/watch?v=tl3OOFpixqs')
driver.maximize_window()
driver.execute_script("window.scrollTo(0, 1000);")
driver.implicitly_wait(10)

#Scrape Title
headlines = driver.find_elements_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
for headline in headlines:
    print(headline.text)

#Scrape views
views = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]')
print(views.text)

#Scrape likes and dislikes
likes = driver.find_elements_by_xpath('//*[@id="text"]')
print(likes[4].text, likes[5].text)

#Scrape date
date = driver.find_element_by_xpath('//*[@id="date"]/yt-formatted-string')
print(date.text)

#Scrape number of comments
driver.implicitly_wait(10)
comments = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string')
print(comments.text)

#Scrape channel id
channel = driver.find_element_by_xpath('//*[@id="text"]/a')
print(channel.text)
print(channel.get_attribute("href"))

driver.close()
# function to download subtitles


def download_subs(url, lang="en"):
    opts = {
        "skip_download": True,
        "writesubtitles": "%(name)s.vtt",
        "subtitlelangs": lang,
        "writeautomaticsub": True
    }
    with youtube_dl.YoutubeDL(opts) as yt:
        yt.download([url])
