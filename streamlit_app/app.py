import streamlit as st
from streamlit_extras.let_it_rain import rain 
import time
from streamlit import session_state as state
from spotify import Spotify
import random
import joblib
from category_encoders import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
import pandas as pd

def loading():
    rain(
        emoji="😭",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )

def preprocessing(data):
    #data['mode'] = data['mode'].astype(str)
    #data['explicit'] = data['explicit'].astype(str)
    if data.loc[0, 'mode']==0:
        data.loc[0,'mode_0']=1
        data.loc[0,'mode_1']=0
    else:
        data.loc[0,'mode_0']=0
        data.loc[0,'mode_1']=1

    if data.loc[0,'explicit']==False:
        data.loc[0, 'explicit_False']=1
        data.loc[0, 'explicit_True']=0
    else:
        data.loc[0, 'explicit_False']=0
        data.loc[0, 'explicit_True']=1

    data=data.drop(columns=['mode','explicit','popularity'])
    encoder = OneHotEncoder(use_cat_names = True)
    data = encoder.fit_transform(data)
    data = data.reindex(sorted(data.columns), axis=1)
    #print(data)
    return data

def scaling(data):
    ctr = ColumnTransformer([('minmax', MinMaxScaler(), ['duration_mins','tempo'])],
                            remainder='passthrough')
    data = ctr.fit_transform(data)
    return data

def get_predictions(data):
    model_path = ''
    model = joblib.load(model_path)
    predictions = model.predict(data)
    return predictions

def main():
    st.title("Predict Your Song")

    artist_name = st.text_input("🎤 Artist")
    song_title = st.text_input("🎶 Track Name")
        
    if st.button("Popularity Prediction"):
        #난수 생성
        random_value = random.choice([0, 1])
        if random_value >= 0.5:
            '''
            #객체 생성
            s = Spotify(artist_name,song_title)
            #변수값 출력
            print(s.getTrackInfo())
            print(s.artist)
            print(s.track)  
            '''

            with st.spinner('Wait for it...'):
                #예측값 받아오기
                #data = [[230666,False,0.676,0.461,1,-6.746,0,0.143,0.0322,1.01e-06,0.358,0.715,87.917,4,0]]
                data={'acousticness':0.0322,'danceability':0.676,'duration_mins':3.8444333333333334,'energy':0.461,'explicit':False,'instrumentalness':1.01e-06,'loudness':-6.746,'mode':0,'popularity':73,'tempo':87.917,'valence':0.715}
                data = pd.DataFrame([data])
                data = preprocessing(data)
                #data = scaling(data)
                #data=[[0.645,0.537,5.51555,0.342,1,0,0.266,-13.553,0,1,109.236,0.253]]
                pred = get_predictions(data)
                #print(pred)
                time.sleep(3)
            st.success(f"Prediction for Artist: {artist_name}, Track Name: {song_title}, Prediction: {pred}")
        else:
            loading()
            st.error("Oops! Something went wrong.")

if __name__ == "__main__":
    main()