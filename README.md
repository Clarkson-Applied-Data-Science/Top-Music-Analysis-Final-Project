# Top-Music-Analysis-Final-Project
Brandon Baker

It is my plan to analyze how music has changed over the years by looking at the top 10 or top 100 songs of each year and comparing data on the nature of these songs. To do this, I will refer to a datasource to create a list of the top songs of the year. This first datasource will likely be the Billboard Top 100 website. To get the data from this source, it looks like I will have to scrape the website. Once I have a list of top songs for each year, I will reference the Spotify API using a module called Spotipy. This API will provide a significant amount of metadata on each song. At this time, I am not settled on any one analysis, and will likely decide for sure when I begin to gather data. At this time, I am interested in metrics such as:
 - Beats Per Minute (Tempo)
 - Song Duration
 - Explicit Label
As well as some more convoluted analysis such as 
 - Dancibility
 - Energy
 - Genre

For reference, below are links to the spotify API information page which shows the structure of the responce as well as a breif description of how these measurements are taken and what they mean:

Get Tracks' Audio Features
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features

Get Track's Audio Features
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features

Get Track's Audio Analysis
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis

