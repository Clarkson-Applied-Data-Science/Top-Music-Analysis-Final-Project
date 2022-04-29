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

| year | danceability | energy | speechiness | instrumentalness | tempo | valence | duration_ms |
| ---- | ------------ | ------ | ----------- | ---------------- | ----- | ------- | ----------- |
| 1960 | 0.5373789473684208 | 0.4755557894736841 | 0.04048421052631579 | 0.030845697894736845 | 120.17663157894738 | 0.680021052631579 | 153814.75789473683
| 1961 | 0.5566161616161617 | 0.47194949494949495 | 0.053452525252525245 | 0.09663090888888888 | 120.97278787878787 | 0.6816868686868687 | 155786.101010101
| 1962 | 0.5636020408163265 | 0.49076734693877555 | 0.055463265306122445 | 0.07570050918367345 | 120.72651020408162 | 0.6806530612244899 | 158599.17346938775
| 1963 | 0.5510505050505052 | 0.513269696969697 | 0.06664848484848483 | 0.07104948828282825 | 118.1460505050505 | 0.7068484848484848 | 156209.101010101
| 1964 | 0.5470103092783506 | 0.5639865979381447 | 0.05037216494845358 | 0.05867370298969075 | 120.57355670103097 | 0.6976381443298968 | 155453.94845360826
| 1965 | 0.5468936170212764 | 0.5552659574468087 | 0.04360212765957446 | 0.05121634436170213 | 119.81815957446801 | 0.6828510638297872 | 165339.5
| 1966 | 0.5485684210526318 | 0.5734947368421053 | 0.04875052631578948 | 0.030573811789473687 | 122.80396842105262 | 0.7111157894736841 | 166059.04210526316
| 1967 | 0.52871875 | 0.5276249999999998 | 0.040484375000000024 | 0.034822437916666664 | 120.41406250000004 | 0.6463541666666668 | 173717.0
| 1968 | 0.552612244897959 | 0.5366326530612244 | 0.05249183673469387 | 0.08362968071428573 | 121.61830612244891 | 0.654048979591837 | 197033.3469387755
| 1969 | 0.5400714285714285 | 0.5120816326530612 | 0.04600306122448981 | 0.033984211836734696 | 116.78717346938777 | 0.6437040816326529 | 192889.10204081633
| 1970 | 0.544949494949495 | 0.5907272727272731 | 0.04873131313131314 | 0.034202738888888896 | 114.21489898989897 | 0.6713838383838386 | 206580.44444444444
| 1971 | 0.5651938775510204 | 0.5520275510204083 | 0.049489795918367344 | 0.028540043877551012 | 115.53223469387758 | 0.672285714285714 | 205124.73469387754
| 1972 | 0.5802244897959183 | 0.5246367346938775 | 0.058726530612244886 | 0.054285713367346965 | 120.32929591836734 | 0.6551530612244898 | 216775.11224489796
| 1973 | 0.56918085106383 | 0.5622021276595747 | 0.05585638297872341 | 0.06805402957446809 | 123.03946808510645 | 0.6953510638297872 | 253817.51063829788
| 1974 | 0.5924183673469388 | 0.5762959183673467 | 0.05362857142857141 | 0.048465933265306134 | 118.99910204081638 | 0.6623153061224492 | 237527.05102040817
| 1975 | 0.5866100000000003 | 0.56091 | 0.04283700000000001 | 0.057069184599999996 | 115.92425999999996 | 0.6615800000000004 | 230307.28
| 1976 | 0.6081546391752579 | 0.6098969072164949 | 0.050991752577319596 | 0.04985647938144326 | 117.76681443298965 | 0.6841237113402063 | 245732.6494845361
| 1977 | 0.5834947368421052 | 0.5836947368421049 | 0.044804210526315794 | 0.046347015157894716 | 120.23316842105257 | 0.6296947368421053 | 236870.64210526316
| 1978 | 0.6099797979797981 | 0.5453676767676766 | 0.0433050505050505 | 0.02283626727272727 | 115.83135353535357 | 0.6204696969696967 | 259154.1717171717
| 1979 | 0.6392121212121213 | 0.595030303030303 | 0.046687878787878785 | 0.05558799151515151 | 121.92259595959595 | 0.7014070707070706 | 259483.8686868687
| 1980 | 0.62513 | 0.5509120000000001 | 0.043938 | 0.03496929259999999 | 121.63578999999999 | 0.655959 | 251641.84
| 1981 | 0.6111938775510205 | 0.548438775510204 | 0.040739795918367336 | 0.01736347979591837 | 119.80359183673465 | 0.5924418367346937 | 241795.76530612246
| 1982 | 0.614105263157895 | 0.5808526315789471 | 0.04316631578947367 | 0.02495141421052632 | 123.74556842105261 | 0.6364273684210525 | 237071.1894736842
| 1983 | 0.6470699999999999 | 0.6330300000000001 | 0.04743400000000001 | 0.023721583300000005 | 121.09640999999999 | 0.6538230000000003 | 256816.07
| 1984 | 0.6589583333333333 | 0.6767638888888889 | 0.04786666666666666 | 0.008653006527777776 | 125.16405555555558 | 0.6709708333333333 | 259359.15277777778
| 1985 | 0.6524057971014493 | 0.6533478260869565 | 0.0419855072463768 | 0.04912661246376812 | 118.47788405797101 | 0.6504782608695655 | 261206.47826086957
| 1986 | 0.6399393939393938 | 0.651060606060606 | 0.041288888888888896 | 0.030381679999999998 | 116.9821414141414 | 0.6558131313131315 | 270188.6767676768
| 1987 | 0.6374639175257729 | 0.6561030927835052 | 0.04221443298969072 | 0.026613913505154633 | 121.50810309278354 | 0.6387731958762887 | 263157.44329896907
| 1988 | 0.6281562499999999 | 0.6581979166666666 | 0.04292708333333333 | 0.011055188854166663 | 118.05965624999999 | 0.6083052083333335 | 263071.7708333333
| 1989 | 0.6280315789473685 | 0.659421052631579 | 0.04971789473684209 | 0.03801622389473685 | 119.5080315789474 | 0.5970736842105265 | 268695.0105263158
| 1990 | 0.6524838709677417 | 0.6672903225806451 | 0.0562279569892473 | 0.017006496666666662 | 116.90269892473114 | 0.6120118279569895 | 277518.1397849462
| 1991 | 0.6259696969696968 | 0.6517575757575759 | 0.05167373737373737 | 0.04895661656565656 | 117.87848484848492 | 0.6063929292929294 | 267948.4646464646
| 1992 | 0.6383838383838386 | 0.631030303030303 | 0.06205555555555553 | 0.021871594444444444 | 119.54858585858587 | 0.5583393939393942 | 275974.0505050505
| 1993 | 0.65023 | 0.6206699999999999 | 0.07021200000000004 | 0.028089556200000004 | 112.97297999999999 | 0.5483099999999997 | 264044.18
| 1994 | 0.6371122448979593 | 0.5967653061224489 | 0.07804489795918368 | 0.022628103571428575 | 120.62570408163265 | 0.5395 | 264744.67346938775
| 1995 | 0.6287173913043476 | 0.6151521739130437 | 0.07394347826086956 | 0.024745739456521726 | 117.08535869565222 | 0.5361576086956521 | 266859.89130434784
| 1996 | 0.6528631578947367 | 0.6350736842105261 | 0.07076947368421051 | 0.03601931442105262 | 113.68151578947374 | 0.5927789473684212 | 263761.0
| 1997 | 0.6667916666666667 | 0.5966291666666667 | 0.07763958333333333 | 0.03827138249999999 | 120.20420833333331 | 0.5582979166666668 | 261000.30208333334
| 1998 | 0.6609255319148936 | 0.5957127659574467 | 0.09793085106382979 | 0.026280850319148938 | 119.15888297872341 | 0.5448638297872341 | 262768.60638297873
| 1999 | 0.6546276595744682 | 0.6352276595744683 | 0.0846851063829787 | 0.001681029680851064 | 112.23052127659578 | 0.5487553191489362 | 257247.414893617
| 2000 | 0.6803510638297872 | 0.7111063829787233 | 0.07106170212765958 | 0.009364364574468086 | 117.53844680851066 | 0.6104712765957445 | 247513.68085106384
| 2001 | 0.6534347826086957 | 0.689532608695652 | 0.08786847826086959 | 0.010068630978260872 | 112.80663043478262 | 0.5754934782608694 | 245786.52173913043
| 2002 | 0.6723369565217391 | 0.7094565217391304 | 0.09879565217391302 | 0.011940563369565213 | 117.51804347826082 | 0.5883826086956524 | 249422.88043478262
| 2003 | 0.6685154639175257 | 0.679144329896907 | 0.13874845360824747 | 0.00818902092783505 | 115.20726804123711 | 0.6058597938144331 | 251512.03092783506
| 2004 | 0.6768969072164949 | 0.6745257731958761 | 0.12144329896907209 | 0.0007030545360824743 | 114.94001030927838 | 0.5886092783505155 | 249572.29896907217
| 2005 | 0.6733958333333336 | 0.6830208333333333 | 0.1242145833333333 | 0.0023672197916666665 | 114.25121875000004 | 0.5513229166666668 | 236472.86458333334
| 2006 | 0.6863100000000002 | 0.6804999999999999 | 0.12954999999999994 | 0.00667238 | 117.51883000000002 | 0.5459369999999999 | 235010.38
| 2007 | 0.6620612244897961 | 0.7183673469387751 | 0.11840918367346936 | 0.009272480408163267 | 120.11314285714286 | 0.5791938775510207 | 244395.52040816325
| 2008 | 0.6484040404040404 | 0.7109898989898993 | 0.0926313131313131 | 0.012896641212121213 | 122.9041111111111 | 0.5192959595959596 | 236300.71717171717
| 2009 | 0.6310303030303034 | 0.7310404040404043 | 0.09136363636363638 | 0.005515404747474746 | 127.5593535353535 | 0.5381818181818181 | 240718.71717171717
| 2010 | 0.63162 | 0.7494700000000001 | 0.09997300000000003 | 0.002871727 | 117.26113000000004 | 0.55007 | 229453.61
| 2011 | 0.6270800000000001 | 0.7517799999999997 | 0.09130600000000005 | 0.0024115563999999993 | 125.94892000000007 | 0.533573 | 234486.5
| 2012 | 0.6451299999999999 | 0.7363699999999997 | 0.08773100000000002 | 0.0026688360999999996 | 127.14731999999998 | 0.55755 | 227114.07
| 2013 | 0.6319484536082473 | 0.7050309278350516 | 0.07428659793814434 | 0.015722497731958763 | 120.83509278350515 | 0.5167546391752575 | 232426.52577319587
| 2014 | 0.6470500000000001 | 0.6924999999999997 | 0.08063400000000001 | 0.006874706600000002 | 120.39119 | 0.5229210000000001 | 230852.26
| 2015 | 0.66399 | 0.655773 | 0.08657399999999997 | 0.0008202265999999998 | 122.53591000000002 | 0.4976799999999997 | 220048.2
| 2016 | 0.66106 | 0.6322249999999999 | 0.11559599999999999 | 0.004302501599999998 | 121.47573000000003 | 0.4544740000000001 | 221819.04
| 2017 | 0.7193299999999999 | 0.6333100000000002 | 0.11946400000000003 | 0.002766041499999999 | 119.33178999999997 | 0.5093309999999999 | 222075.74
| 2018 | 0.7222999999999997 | 0.6314199999999998 | 0.121678 | 0.0015851694000000001 | 121.1274 | 0.45155199999999995 | 212243.83
| 2019 | 0.7162099999999999 | 0.61691 | 0.13203200000000007 | 0.0064029922999999985 | 119.03413000000002 | 0.4803569999999999 | 193749.51
| 2020 | 0.6948900000000002 | 0.6063099999999999 | 0.12120400000000002 | 0.0080127515 | 119.69052999999998 | 0.4880570000000002 | 196517.37
| 2021 | 0.6864299999999995 | 0.63424 | 0.120251 | 0.005941117000000001 | 116.51241000000002 | 0.5117869999999997 | 194813.71








