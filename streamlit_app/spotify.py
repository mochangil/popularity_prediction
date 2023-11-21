import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

class Spotify:

    def __init__(self, artist, track):
        self.artist = artist
        self.track = track

    @st.cache_data
    def getTrackInfo(_self):
        
        client_credentials_manager = SpotifyClientCredentials(client_id='084ce5e33c774221b1c77d495a78ea70', client_secret='c9fdf6bdc0864e149b4bd447ec28f605')
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        artist_name =[]
        track_name = []
        track_popularity =[]
        artist_id =[]
        track_id =[]
        track_duration = []
        track_explicit = []
        track_results = []
        for i in range(0,50,5):
            track_results = sp.search(q='artist:'+_self.artist, type='track', limit=5, offset=i)
            if(len(track_results)):
                for i, t in enumerate(track_results['tracks']['items']):
                    artist_name.append(t['artists'][0]['name'])
                    artist_id.append(t['artists'][0]['id'])
                    track_name.append(t['name'])
                    track_id.append(t['id'])
                    track_popularity.append(t['popularity'])
                    track_duration.append(t['duration_ms'])
                    track_explicit.append(t['explicit'])
                    

      
        track_df = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_id, 'track_popularity' : track_popularity, 'artist_id' : artist_id, 'explicit' : track_explicit})

        track_info = pd.DataFrame()
        track_features = pd.DataFrame()
        track_info = track_df[track_df['track_name']==_self.track]
        
        track_features = sp.audio_features(track_info['track_id'])
        #log
        print("track_features",track_features)

        track_features = pd.DataFrame(track_features)
        track_features['popularity'] = track_info['track_popularity']
        track_features['explicit'] = track_info['explicit']
        cols_to_drop = ['id','track_href','analysis_url','uri','type']
        track_features = track_features.drop(columns = cols_to_drop)

        #model에 맞춰 column 재구성
        track_features = track_features[['duration_ms','explicit','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']]      
        
        return track_features


