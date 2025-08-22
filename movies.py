import streamlit as st
import pandas as pd
import numpy as np
import requests
import pickle
from PIL import Image # For displaying images

# Custom CSS to style the button
st.markdown("""
<style>
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
    }
    .stButton > button:hover {
        background-color: #FF0000;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


with open('movies.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = movies.index[movies['title'] == title][0]  # get the index of the movie
        sim_scores = list(enumerate(cosine_sim[idx]))  # get the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # sort
        sim_scores = sim_scores[1:11]  # get top 10
        movie_indices = [i[0] for i in sim_scores]  # get indices
        return movies.iloc[movie_indices]  # Return the FULL DataFrame rows, not just titles
    except IndexError:
        st.error(f"Movie '{title}' not found in database")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

def fetch_poster(movie_id):
    try:
        api_key = '69d4782fa1fa0b10972c99032be69ea5'
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
        response = requests.get(url)
        data = response.json()
        poster_path = data['poster_path']  
        full_path = f'https://image.tmdb.org/t/p/w500{poster_path}' if poster_path else None
        return full_path
    except:
        return None  # Return None if poster can't be fetched

st.image("film.png",  width=700)

st.title('NeuroFlix Movie Recommendation System🎬🍿')
selected_movie = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    
    if recommendations.empty:
        st.write("No recommendations available.")
    else:
        st.write('Top 10 Recommended Movies🔥')
        
        # Create a grid layout
        for i in range(0, 10, 5):  # 2 rows of 5 columns each
            cols = st.columns(5)
            for col, j in zip(cols, range(i, i+5)):
                if j < len(recommendations):
                    movie_title = recommendations.iloc[j]['title']
                    movie_id = recommendations.iloc[j]['movie_id']  # This should work now
                    poster_url = fetch_poster(movie_id)
                    
                    with col:
                        if poster_url:
                            st.image(poster_url, width=130, caption=movie_title)
                        else:
                            st.write(movie_title)
                            st.write("(Poster not available)")
                else:
                    with col:
                        st.write("")  # Empty space for alignment