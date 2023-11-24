import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

class Spotify:

    def __init__(self, artist, track, img):
        self.artist = artist
        self.track = track
        self.img = img

    @st.cache_data
    def getTrackInfo(_self):
        
        client_credentials_manager = SpotifyClientCredentials(client_id='b23490441d814051a9418a8d8498e2db', client_secret='c1b805f73a9c4f23847edf9263baeb42')
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        artist_name =[]
        track_name = []
        track_popularity =[]
        artist_id =[]
        track_id =[]
        track_duration = []
        track_explicit = []
        track_results = []
        track_img = []
        for i in range(0,100,50):
            track_results = sp.search(q='artist:'+_self.artist, type='track', limit=50, offset=i)
            if(len(track_results)):
                for i, t in enumerate(track_results['tracks']['items']):
                    print(t['artists'])
                    artist_name.append(t['artists'][0]['name'])
                    artist_id.append(t['artists'][0]['id'])
                    track_name.append(t['name'])
                    track_id.append(t['id'])
                    track_popularity.append(t['popularity'])
                    track_duration.append(t['duration_ms'])
                    track_explicit.append(t['explicit'])
                    track_img.append(t['album']['images'][1]['url'])

                    

      
        track_df = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_id, 'track_popularity' : track_popularity, 'artist_id' : artist_id, 'explicit' : track_explicit, 'album_img_url':track_img})
        # print(track_df['track_name'])
        track_info = pd.DataFrame()
        track_features = pd.DataFrame()
        track_info = track_df[track_df['track_name']==_self.track]
        # print("track_info :", len(track_info['album_img_url']))
        # print("---------------------------------------------")
        # if(track_info['album_img_url'])
        _self.img = (list(track_info['album_img_url']))[0]
        # print("img_url :",_self.img)
        track_features = sp.audio_features(track_info['track_id'])

        track_features = pd.DataFrame(track_features)
        track_features['popularity'] = track_info['track_popularity']
        track_features['explicit'] = track_info['explicit']
        cols_to_drop = ['id','track_href','analysis_url','uri','type']
        track_features = track_features.drop(columns = cols_to_drop)
        print("popularity:",track_features['popularity'])
        
        #model에 맞춰 column 재구성
        # track_features = track_features[['duration_ms','explicit','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature','popularity']]      
        track_features = track_features[['duration_ms','explicit','danceability','energy','loudness','acousticness','valence','tempo','mode','popularity']]      
        # sample default value
        track_features['duration_mins']=[30.01]
        return track_features


