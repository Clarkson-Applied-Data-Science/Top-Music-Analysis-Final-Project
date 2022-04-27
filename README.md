# Top-Music-Analysis-Final-Project
Brandon Baker

It is my plan to analyze how music has changed over the years by looking at the top 10 or top 100 songs of each year and comparing data on the nature of these songs. To do this, I will refer to a datasource to create a list of the top songs of the year. This first datasource will likely be the Billboard Top 100 website. To get the data from this source, it looks like I will have to scrape the website. Once I have a list of top songs for each year, I will reference the Spotify API using a module called Spotipy. This API will provide a significant amount of metadata on each song. At this time, I am not settled on any one analysis, and will likely decide for sure when I begin to gather data. At this time, I am interested in metrics such as:
 - Beats Per Minute (Tempo)
 - Song Duration
 - Explicit Label

As well as some more convoluted analysis such as:
 - Dancibility
 - Energy
 - Genre

For reference, below are links to the spotify API information page which shows the structure of the response as well as a breif description of how these measurements are taken and what they mean:

Get Tracks' Audio Features
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features

Get Track's Audio Features
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features

Get Track's Audio Analysis
https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis

# The Actual Project
Setting out to see how music changes over time, I created a series of information-gathering python scripts to create one library of music and it's features. 

The process started by gathering the names and artists of the top 100 songs of a given year. For this, I initally turned to the Billboard Top 100, searching for an API or some pattern in the website that I could scrape. Unfortunatly, there was no such resource readily availble over any length of time that would be of interest. At this point, I found that Wikipedia had a series of websites that would list the Billboard Top 100. I decided that this is what I would scrape for the track names and artists.

A little research on the Spotify API showed that a track name and artist would not suffice for requesting information from the API. I first needed a unique identifier for the song. Additionally, I would need a token to access the API information. Searching through the documentation and the web, I found a method for searching for the ID using the artist and track names. Thus I was able to verify that my analysis was possible. Using this method, I obtained the song ID and then, using that ID, I could request the information I was after from the API.

#Scraping Wikipedia
The source of the top 100 came from the following website:
https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}
where {year} should be replaced with the four-digit year in question. This source was the deciding factor for the year range I chose. When inputing the year 1958, the length of the list on Wikipedia was 50 and after 1958, the list was 100 long. For the ease of scraping, I decided to make 1959 the first year in the range. Furthermore, having run this script in the middle of 2022, the top 100 for 2022 would not be populated yet, so 2021 was determined to be the minimum year. 

The program would iterate through all of the years in this range and request the HTML for each page. Looking through the pages, there were several key discoveries I made that would influence how I gathered the information from these pages. 
- There were not a lot of identifiers that would allow BeautifulSoup to quickly and accuratly find the portion of the HTML that would be useful. This would cause me to use the split method instead. 
- There was a handy table which included all 100 songs and their artist, but the syntax in these sections was inconsistent between other items in that table and also inconsistent between pages. This would eventually lead to using the try/except method in the script.

The program first split the HTML to only inlcude the table of songs and aritsts. Then the table was split again with a delimeter that would break the table into 100 "rows." In reality, each "row" had four rows to it, where the second contained the name of the song (called the song row) and the third contained the name of the aritst (called the artist row). The reason I call this a "row" however, is because it broke the table into the 100 instances of songs for that year. 

To the song out of the row, I split to the song row. The song name often appeared more than once in the song row. The last instance of the song name often proved to be the "cleanest" as other isntances would often contain special characters to represent ampersands or apostropies. To get at the cleanest version of the song name, I had the script count the number of times the word "title" appeared in the song row, as "title" would appear before each instance of the song name. Once the script had a count, I split to be after the last instance, and would get the song name this way. Some song rows did not have any instances of "title" so, a condition was created to split to the song name using the syntax of these rows. The song name would often still have a few errors in it, such as the string: "&amp;" appearing where there should just be an ampersand, so a replace condition was created to swap the error with the correct symbol. 

The aritst name proved to be more varied in syntax than the song name was. For this reason, try/except was used to catch a few of the variations, the most common of which was first. If the first method failed, another method was attempted. There was one more layer below that. Each layer used a combination of splits to widdle down the artist row until only the artist name was left. Like the song, the artist name was cleaned to remove the ampersand identifier which identified a speacial character and replace it with the actual ampersand character. 

These variables were added to a dictionary called song_data. Furthermore, the song and artist were combined into one string seperated by a space. This variable will be used to lookup the ID for spotify. 

#Spotify Authentication, ID Search, and Go/No Go Poll
In order to access information from spotify, there are some extra steps required. First, a token is required. To obtain a token, I had to go to the spotify API documentation and request a token from the console section. I stored this string as a variable called token. 

I needed to find a way to apply this token with the appropriote syntax and to search for the required ID to query specific songs. While the spotify documentation was very thourough, I found the following source to explain how to apply this token and to search for a song's ID (link below).
https://www.youtube.com/watch?v=R3XgZ__jQxw&t=920s
This source pointed me to use the following link https://api.spotify.com/v1/search?q={lookup}&type=track where {lookup} is essentially what you would type into the search option in the spotify UI to find a song. In this case, I would use the variable that contained both the song and artist. The video intially used a module called urllib to convert this variable to the correct syntax for searching this webpage. Instead of using this method however, I decided to dig into what urllib was doing in this case and removed the need for the module by replacing all spaces in this variable with "%20". The output from this request was a json. 
At this point, there were several checks that must be completed. The response from the request was a list of possible songs that the search could lead to. If the search had no results, it would return with an error. The first check was to try and index the response at "error." This key would only appear if the search failed. A variable called "go" was created prior to this try/except and set to False. 

If the index failed (meaning that the search succeeded), "go" was set to True, clearing the program to lookup values for the song. It is worth noting here that with this try/except, "go" was only set to True in the event of a key error. In the event that the index failed, a key was created in the song_data dictionary for the ID and the first result from the responce was used. I created it this way assuming that the best match for the search would be the first one listed. Other failings of the index would stop the program as usual. 

If the index to "error" suceeded, this means that the search failed, and "go" would be left as False. Ultimatly, this would result in all variables other than the song and artist names being set to None.

#Spotify Data Gathering
If the program was cleared by the Go/No Go poll, it would next set out to find the data on that song using the ID. According to the Spotify API, the following url was used https://api.spotify.com/v1/audio-features/'+results[0]['id'] where results[0]['id'] was the first ID in the list of possible ID's from the response above (explainition above). The response was a lengthy json. This time, I indexed at the stats of interest and added them to the song_data dictionary. These values are listed below. Also included is the description of these values from the Spotify API. 
- danceability
  -"Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable."
- energy
  -"Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy"
- speechiness
  -"Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks."
- instrumentalness
  -"Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0."
- tempo
  -"The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration."
- valence
  -"A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."
- duration_ms
  -"The duration of the track in milliseconds"

All descriptions are direct quotes from the Spotify API Developer webpage linked here: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features

Each value was populated into song_data if it passed a try/except. On an error, the field would populate as None. 

Finally, I added the song's "place" to the song_data dictionary. The "place" was essentially which number it placed on the Top 100 list, so the most popular song for a given year was given a place of 1. This was done by incimenting a variable "n" for each time the program looped to look at the next song.

Now with a dictionary containing all of the information pertaining to a year's top 100 songs, I added song_data to a larger dictionary where the index is the year. 

The year was incrimented and the loop would repeat. Once the max year was run, the loop would end and the resulting json was dumped into a .json file saved locally. This would allow analysis of the data without needing to run the program again (the program took ~45 minutes to run on hotel wifi on my older laptop).

#The Analysis










