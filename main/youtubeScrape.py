import youtube_dl
from selenium import webdriver
import pandas as pd
import datetime as dt
from youtube_transcript_api import YouTubeTranscriptApi as yta


def video_scrape(url):

    # Setup
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, 500);")
    driver.implicitly_wait(10)
    data = {}

    # Scrape channel id
    channel = driver.find_element_by_xpath('//*[@id="text"]/a')
    link = channel.get_attribute("href")[32:]
    data['Channel ID'] = link
    data['Channel name'] = channel.text

    # Scrape Title
    headlines = driver.find_elements_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
    data['Video ID'] = url[32:]
    data['Video Title'] = headlines[0].text

    # Scrape views
    views = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]')
    number = int(views.text[:-8].replace(".", ""))
    data['Views'] = number

    # Scrape likes and dislikes
    rating = driver.find_elements_by_xpath('//*[@id="text"]')
    likes = int(rating[4].text.replace(".", ""))
    dislikes = int(rating[5].text.replace(".", ""))
    data['Likes'] = likes
    data['Dislikes'] = dislikes

    # Scrape date
    dat = driver.find_element_by_xpath('//*[@id="date"]/yt-formatted-string')
    date_str = ''.join(ch for ch in dat.text if ch.isdigit())
    date_dat = dt.datetime(int(date_str[-4:]), int(date_str[2:-4]), int(date_str[0:2]))
    data['Upload Date'] = date_dat.isoformat()

    # Scrape length in seconds
    length = driver.execute_script(
                        "return document.getElementById('movie_player').getDuration()")
    data['Duration'] = int(length)

    # Scrape number of comments
    driver.implicitly_wait(10)
    comments = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string')
    comment_number = int(''.join(ch for ch in comments.text if ch.isdigit()))
    data['Number of Comments'] = comment_number

    # Scrape captions
    # Create a new file
    f = open("C:\\Users\\matia\\youtubeScrape\\Captions\\" + url[32:] + '.txt', 'w+')

    # Scrape and write into file
    out, _ = yta.get_transcripts([url[32:]])
    text_out = {}
    text_out = ' '.join([x.get('text', '') for x in out[url[32:]]])
    f.write(text_out)
    f.close()


    driver.close()
    return data


video_scrape("https://www.youtube.com/watch?v=Jmr0uCTKi9o&t=7s")

def channel_scraper(url):




    def download_subs(url, lang="en"):
        opts = {
            "skip_download": True,
            "writesubtitles": "%(name)s.vtt",
            "subtitlelangs": lang,
            "writeautomaticsub": True
        }
        with youtube_dl.YoutubeDL(opts) as yt:
            yt.download([url])
