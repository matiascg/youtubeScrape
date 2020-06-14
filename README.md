# YoutubeScrape

The goal of YoutubeScrape is to get data about YouTube-videos and channels. The idea was to use the YouTube API to get this information, but because of the quota usage of the API, this is no longer an option. Because of this the new plan is to scrape the html for most of this information and use other libraries (like youtube_dl) to get the rest.
The data needed from this project is:


**From the videos**

•	Channel id / (channel name)

•	Video id

•	Video name

•	Upload date

•	Tags

•	View-count

•	Likes/dislikes/comments

•	Captions (To be analyzed separately for matches of Channel names)

•	Video-length

•	Category


**From the channels**

•	Channel id

•	Viewcount

•	Subscriber-count

•	Creation-date

•	Number of Uploads


The collection of this data must be automated for Channels, so that the program is able to go through a list with Channel ids and extract all the information from all the videos. In the best case the program should be able to extract information at various time points for each specific channel and video. The data will be entered into a Dataframe, with an exception being the captions, which must be analyzed for connections to other channels in order to be of any significance.
The project is written in Python, it uses libraries like requests and BeautifulSoup to scrape the html, Pandas to put the data in Dataframes and various others to help with the process. To help manage dependencies Anaconda is used, and it could be the case that the project will shift to use the Selenium Framework to make it easier and faster to access data directly from the browser.
