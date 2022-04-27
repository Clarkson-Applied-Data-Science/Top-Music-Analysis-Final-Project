#Spotify Data Analysis
import json, matplotlib.pyplot as plt
f=open('spotify_json_data.json')
Top100=json.load(f)

'''
for year in Top100:
    print(year)
    for song in Top100[year]:
        print(song)
'''
all_years_data={}
y_danceability={}
y_energy={}
y_speechiness={}
y_instrumentalness={}
y_tempo={}
y_valence={}
y_duration_ms={}
years=[]
for year in Top100:
    year_data={}
    danceability_sum=0
    danceability_count=0
    energy_sum=0
    energy_count=0
    speechiness_sum=0
    speechiness_count=0
    instrumentalness_sum=0
    instrumentalness_count=0
    tempo_sum=0
    tempo_count=0
    valence_sum=0
    valence_count=0
    duration_ms_sum=0
    duration_ms_count=0
    for song in Top100[year]:
        #print(song,Top100[year][song]['track'])
        if Top100[year][song]['danceability']!=None:
            danceability_sum+=Top100[year][song]['danceability']
            danceability_count+=1
        if Top100[year][song]['energy']!=None:
            energy_sum+=Top100[year][song]['energy']
            energy_count+=1
        if Top100[year][song]['speechiness']!=None:
            speechiness_sum+=Top100[year][song]['speechiness']
            speechiness_count+=1
        if Top100[year][song]['instrumentalness']!=None:
            instrumentalness_sum+=Top100[year][song]['instrumentalness']
            instrumentalness_count+=1
        if Top100[year][song]['tempo']!=None:
            tempo_sum+=Top100[year][song]['tempo']
            tempo_count+=1
        if Top100[year][song]['valence']!=None:
            valence_sum+=Top100[year][song]['valence']
            valence_count+=1
        if Top100[year][song]['duration_ms']!=None:
            duration_ms_sum+=Top100[year][song]['duration_ms']
            duration_ms_count+=1
    year_danceability=danceability_sum/danceability_count
    year_danceability_err=100-danceability_count
    year_energy=energy_sum/energy_count
    year_energy_err=100-energy_count
    year_speechiness=speechiness_sum/speechiness_count
    year_speechiness_err=100-speechiness_count
    year_instrumentalness=instrumentalness_sum/instrumentalness_count
    year_instrumentalness_err=100-instrumentalness_count
    year_tempo=tempo_sum/tempo_count
    year_tempo_err=100-tempo_count
    year_valence=valence_sum/valence_count
    year_valence_err=100-valence_count
    year_duration_ms=duration_ms_sum/duration_ms_count
    year_duration_ms_err=100-duration_ms_count
    year_data['year_danceability']=year_danceability
    year_data['year_danceability_err']=year_danceability_err
    year_data['year_energy']=year_energy
    year_data['year_energy_err']=year_energy_err
    year_data['year_speechiness']=year_speechiness
    year_data['year_speechiness_err']=year_speechiness_err
    year_data['year_instrumentalness']=year_instrumentalness
    year_data['year_instrumentalness_err']=year_instrumentalness_err
    year_data['year_tempo']=year_tempo
    year_data['year_tempo_err']=year_tempo_err
    year_data['year_valence']=year_valence
    year_data['year_valence_err']=year_valence_err
    year_data['year_duration_ms']=year_duration_ms
    year_data['year_duration_ms_err']=year_duration_ms_err
    #print(year)
    all_years_data[year]=year_data
    
    years.append(year)
    y_danceability[year]=year_danceability
    y_energy[year]=year_energy
    y_speechiness[year]=year_speechiness
    y_instrumentalness[year]=year_instrumentalness
    y_tempo[year]=year_tempo
    y_valence[year]=year_valence
    y_duration_ms[year]=year_duration_ms
#print(all_years_data)
#print(y_danceability)

f.close
