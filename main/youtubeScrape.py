import youtube_dl
from selenium import webdriver
import pandas as pd
import datetime as dt
from youtube_transcript_api import YouTubeTranscriptApi as yta


def video_scrape(url, driver):

    # Setup
    driver.get(url)
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
    text_out = ' '.join([x.get('text', '') for x in out[url[32:]]])
    f.write(text_out)
    f.close()

    return data


def channel_list_creator(driver):
    driver.get('https://socialblade.com/youtube/top/5000/mostsubscribed')
    data = {'Channel name': [], 'Channel ID': []}
    driver.implicitly_wait(10)
    links = []

    for i in range(5, 10):
        channels = driver.find_element_by_xpath('/html/body/div[11]/div[2]/div[' + str(i) + ']/div[3]/a')
        if not str(driver.find_element_by_xpath('/html/body/div[11]/div[2]/div[' + str(i) + ']/div[4]/span').text) == '--':
            links.append(channels.get_attribute('href'))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    for link in links:
        driver.get(link)
        name = driver.find_element_by_xpath('//*[@id="YouTubeUserTopInfoBlockTop"]/div[1]/h1')
        data['Channel name'].append(name.text)
        i = 1
        while True:
            channel_link = str(driver.find_element_by_xpath('//*[@id="YouTubeUserTopSocial"]/div[' + str(i) + ']/a').get_attribute(
                'href'))
            i += 1
            if channel_link.startswith('https://youtube.com/channel/'):
                break
        data['Channel ID'].append(channel_link.split("channel/", 1)[1])

    return data


def channel_scraper(channel_id, driver):

    # Set up
    url = 'https://youtube.com/channel/' + channel_id + '/videos'
    video_info = {'Video ID': [], 'Title': []}
    driver.get(url)
    driver.implicitly_wait(10)

    # Adding Name and ID
    name = driver.find_elements_by_xpath('//*[@id="text"]')[3]
    channel_info = {'Channel ID': [channel_id], 'Channel name': [name.text]}

    # Adding Subscribers
    abos = str(driver.find_element_by_xpath('//*[@id="subscriber-count"]').text)

    # Translating to int
    if 'Mio' in abos:
        abos = abos.partition('Mio')[0]
        if ',' in abos:
            abos = abos.replace(',', '.')
        abos_number = int(abos) * 1000000
    else:
        abos = abos.partition('Abon')[0]
        abos_number = int(abos)
    channel_info['Subscribers'] = [abos_number]

    # Adding Video ID and Title
    videos = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for video in videos:
        video_info['Title'].append(video.text)
        video_info['Video ID'].append(str(video.get_attribute('href')).split('watch?v=', 1)[1])
    channel_info['Videos'] = [video_info]

    # Creating a DataFrame
    data = pd.DataFrame(channel_info)

    return data


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


def multi_scrape(lst, driver):
    tab = pd.DataFrame(columns=['Channel ID', 'Channel name', 'Subscribers', 'Videos'])
    for channel in lst['Channel ID']:
        tab = tab.append(channel_scraper(channel, driver), ignore_index=True)
    print(tab)

#tab = pd.DataFrame(channel_scraper('UCq-Fj5jknLsUf-MWSy4_brA'))
#tab = tab.append(channel_scraper('UCtmqhpXgTzLJBVo5_LMAHHw'), ignore_index=True)
#print(tab)




