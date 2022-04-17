import requests, urllib, spotipy, json

#1959 is the first year with a list of 100
year_min=1960
year_max=2021
top100={}
token='BQCmZe7AlYL3mX_ZquxQ0o-ol6nFBwe7pxmx-LkIeB-mybjiBsUT-DzElbLlK4DEqDbB7Q-Fn9mJxQUnhIUF5LN1TajztkBMtlzNjV8Raz4mPBTyfr0gFUkl_tvmcKUsg3OntJg3FClTowO8hf0H7fX7'


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
                song_data={}
                song_row=row.split('<td>')[2]
                title_count=song_row.count('title=')
                if title_count != 0:
                    song=song_row.split('title="')[title_count].split('</a>"</td>')[0].split('">')[1].split('</a>')[0]
                    song=song.replace('&amp;','&')
                else:
                    song=song_row.split('"')[1].split('"</td>')[0]
                    song=song.replace('&amp;','&')
                artist=row.split('<td>')[3].split('title="')[1].split('">')[0].split(' (')[0]
                artist=artist.replace('&amp;','&')
                
                song_data['track']=song
                song_data['artist']=artist
                track_artist=song+' '+artist
                
                lookup=track_artist.replace(' ','%20')
                url=f'https://api.spotify.com/v1/search?q={lookup}&type=track'
                responce=requests.get(
                    url,
                    headers={
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {token}'
                    }
                )
                responce_json=responce.json()
                results=responce_json['tracks']['items']
                if results:
                    song_data['id']=results[0]['id']
                    url='https://api.spotify.com/v1/audio-features/'+results[0]['id']
                    responce=requests.get(
                        url,
                        headers={
                                'Content-Type': 'application/json',
                                'Authorization': f'Bearer {token}'
                        }
                    )
                    responce_json=responce.json()
                    song_data['id']=results[0]['id']
                    song_data['danceability']=responce_json['danceability']
                    song_data['energy']=responce_json['energy']
                    song_data['speechiness']=responce_json['speechiness']
                    song_data['instrumentalness']=responce_json['instrumentalness']
                    song_data['tempo']=responce_json['tempo']
                    song_data['valence']=responce_json['valence']
                    song_data['duration_ms']=responce_json['duration_ms']
                else:
                    song_data['id']='no results'
                    
                    song_data['id']=''
                    song_data['danceability']=''
                    song_data['energy']=''
                    song_data['speechiness']=''
                    song_data['instrumentalness']=''
                    song_data['tempo']=''
                    song_data['valence']=''
                    song_data['duration_ms']=''
                    

                song_place[n]=song_data
                print(song_data)
            n+=1
    top100[year]=song_place
    year+=1
print(top100)
with open('spotify_json_data.json','w') as json_out:
    json.dump(top100,json_out)