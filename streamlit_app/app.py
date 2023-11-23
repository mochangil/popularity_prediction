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
from pathlib import Path

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
    '''
    if data.loc[0, 'mode']==0:
        data.loc[0,'mode_0']=1
        data.loc[0,'mode_1']=0
    else:
        data.loc[0,'mode_0']=0
        data.loc[0,'mode_1']=1
    '''

    if data.loc[0,'explicit']==False:
        data.loc[0, 'explicit_False']=1
        data.loc[0, 'explicit_True']=0
    else:
        data.loc[0, 'explicit_False']=0
        data.loc[0, 'explicit_True']=1

    data["duration_mins"] = data["duration_ms"]/60000

    data=data.drop(columns=['mode','explicit','popularity'])
    encoder = OneHotEncoder(use_cat_names = True)
    data = encoder.fit_transform(data)
    data = data.reindex(sorted(data.columns), axis=1)
    data = data.drop(columns=['duration_ms'])
    #print(data)
    return data

def scaling(data):
    ctr = ColumnTransformer([('minmax', MinMaxScaler(), ['duration_mins','tempo'])],
                            remainder='passthrough')
    data = ctr.fit_transform(data)
    return data

def get_predictions(data):
    model_path = Path(__file__).parent
    model_path = model_path/'nonscale_model.pkl'
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
            #객체 생성
            s = Spotify(artist_name,song_title)
            # print(s.artist)
            # print(s.track)  

            with st.spinner('Wait for it...'):
                #예측값 받아오기
                data = s.getTrackInfo()
                data = preprocessing(data)
                pred = get_predictions(data)
                #data = scaling(data)
                #print(pred)
                time.sleep(3)
            st.success(f"Predicted Popularity Level for {song_title} by {artist_name} is {pred}")
        else:
            loading()
            st.error("Oops! Something went wrong.")

if __name__ == "__main__":
    main()
