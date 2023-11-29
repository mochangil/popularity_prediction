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

    scaler = StandardScaler()
    data[['duration_ms','danceability','energy','loudness','acousticness','valence','tempo']] = \
        scaler.fit_transform(data[['duration_ms','danceability','energy','loudness','acousticness','valence','tempo']])
    '''
    if data.loc[0, 'mode']==0:
        data.loc[0,'mode_0']=1
        data.loc[0,'mode_1']=0
    else:
        data.loc[0,'mode_0']=0
        data.loc[0,'mode_1']=1
    '''
    if data.loc[0,'explicit']==False:
        data.loc[0, 'Category_False']=1
        data.loc[0, 'Category_True']=0
    else:
        data.loc[0, 'Category_False']=0
        data.loc[0, 'Category_True']=1

    data=data.drop(columns=['explicit'])
    #encoder = OneHotEncoder(use_cat_names = True)
    #data = encoder.fit_transform(data)
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
    model_path = model_path/'best_model.pkl'
    model = joblib.load(model_path)
    predictions = model.predict(data)
    return predictions

def main():
    if st.button("🌊 Rerun"):
        st.rerun()

    
    st.title("Predict Your Song")

    artist_name = st.text_input("🎤 Artist")
    song_title = st.text_input("🎶 Track Name")
        
    if st.button("Popularity Prediction"):
        #난수 생성
        #객체 생성
        s = Spotify(artist_name,song_title,"1")
        # print(s.artist)
        # print(s.track)  
        print(s.img)
        with st.spinner('Wait for it...'):
            #예측값 받아오기
            try:
                data = s.getTrackInfo()
                data = preprocessing(data)
                pred = get_predictions(data)
                print(pred)
                try:
                    st.image(s.img)
                except:
                    st.warning("Sorry, no image available")

                if(1):
                    if pred == 1:
                        st.success('💻 Predicted Popularity Level : 1 (1/1, popular!)')                
                    else :
                        st.success('📺 Predicted Popularity Level : 0 (0/1, unpopular)')
                    #data = scaling(data)
                    #print(pred)
                        time.sleep(3)
            except:
                st.warning("Sorry, please try with another song")
        
        st.cache_data.clear()        
if __name__ == "__main__":
    main()
