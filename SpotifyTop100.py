import requests, spotipy, json

#1959 is the first year with a list of 100
year_min=1960
year_max=2021
top100={}
token='BQCzinkZxXmzNOH9tocN2oMIxJB7JE8iXbaKxiYMQ1QWm2pY98lH1Ps3Qa88EwXqlJO9dhdF5dHERmiQzAVeNTIo_OVgeKLGoXz5nHQ8rGtNM8Yvd2QcYStK3Bg0_WygE1tNuqh9aSUYp5rwlkeO9DNF'

year=year_min
while year<=year_max:
    print(year)
    years_data={}
    url=f'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}'
    r=requests.get(url)
    table=r.text.split('</th></tr>')[1].split('</td></tr></tbody></table>')[0]
    n=0
    rows=table.split('<tr>')
    song_place={}
    for row in rows:
        if n!=101:
            if n!=0:
                #response_json=None
                #response=None
                song_data={}
                #print(n,row)
                song_row_fail=False
                try:
                    song_row=row.split('<td>')[2].split('</td>')[0]
                except:
                    song_row=row.split('<td')[2].split('</td>')[0]
                #print(song_row)
                title_count=song_row.count('title=')
                if title_count != 0:
                    song=song_row.split('title="')[title_count].split('</a>"</td>')[0].split('">')[1].split('</a>')[0]
                    song=song.replace('&amp;','&')
                else:
                    song=song_row.split('"')[1].split('"</td>')[0]
                    song=song.replace('&amp;','&')
                try:
                    artist=row.split('<td>')[3].split('title="')[1].split('">')[0].split(' (')[0]
                except:
                    try:
                        artist=row.split('<td')[3].split('title="')[1].split('">')[0].split(' (')[0]
                    except:
                        artist=row.split('<td>')[1]
                artist=artist.replace('&amp;','&')
                
                song_data['track']=song
                song_data['artist']=artist
                track_artist=song+' '+artist
                
                lookup=track_artist.replace(' ','%20')
                url=f'https://api.spotify.com/v1/search?q={lookup}&type=track'
                response=requests.get(
                    url,
                    headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {token}'
                    }
                )
                response_json=response.json()
                go=False
                results=[]
                try:
                    results=response_json['error']
                except KeyError as e:
                    go=True
                    results=response_json['tracks']['items']
                #print(results)
                if go and len(results)>0:
                    song_data['id']=results[0]['id']
                    print(results[0]['id'])
                    url='https://api.spotify.com/v1/audio-features/'+results[0]['id']
                    response=requests.get(
                        url,
                        headers={
                                'Content-Type': 'application/json',
                                'Authorization': f'Bearer {token}'
                        }
                    )
                    response_json=response.json()
                    song_data['id']=results[0]['id']
                    try:
                        song_data['danceability']=response_json['danceability']
                    except:
                        song_data['danceability']=None
                    try:
                        song_data['energy']=response_json['energy']
                    except:
                        song_data['energy']=None
                    try:
                        song_data['speechiness']=response_json['speechiness']
                    except:
                        song_data['speechiness']=None
                    try:
                        song_data['instrumentalness']=response_json['instrumentalness']
                    except:
                        song_data['instrumentalness']=None
                    try:
                        song_data['tempo']=response_json['tempo']
                    except:
                        song_data['tempo']=None
                    try:
                        song_data['valence']=response_json['valence']
                    except:
                        song_data['valence']=None
                    try:
                        song_data['duration_ms']=response_json['duration_ms']
                    except:
                        song_data['duration_ms']=None

                else:
                    song_data['id']='no results'
                    
                    song_data['id']=None
                    song_data['danceability']=None
                    song_data['energy']=None
                    song_data['speechiness']=None
                    song_data['instrumentalness']=None
                    song_data['tempo']=None
                    song_data['valence']=None
                    song_data['duration_ms']=None
                    
                song_place[n]=song_data
                print(song_data)
                print('---------------------------------------')
            n+=1
    top100[year]=song_place
    year+=1
print(top100)
with open('spotify_json_data.json','w') as json_out:
    json.dump(top100,json_out)