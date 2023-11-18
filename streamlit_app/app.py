import streamlit as st
from streamlit_extras.let_it_rain import rain 
import time
from streamlit import session_state as state
from spotify import Spotify

def loading():
    rain(
        emoji="🎧",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )

def main():
    st.title("hiiiii")

    artist_name = st.text_input("🎤 Artist")
    song_title = st.text_input("🎶 Track Name")
    result_placeholder = st.empty()

    if st.button("Popularity Prediction"):

        #객체 생성
        s = Spotify(artist_name,song_title)
        #변수값 출력
        print(s.getTrackInfo())
        print(s.artist)
        print(s.track)  
        
        #loading()
        with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success(f"Prediction for Artist: {artist_name}, Track Name: {song_title}")

if __name__ == "__main__":
    main()