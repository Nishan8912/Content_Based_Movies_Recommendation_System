import requests
import streamlit as st
import pickle
import pandas as pd

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_list['title'].values
new_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=6aae2f32e96e1685f4f375b94798c8d5'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_lists = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommended_movies_poster = []
    for li in movies_lists:
        movie_id = new_df.iloc[li[0]].movie_id
        recommend_movies.append(new_df.iloc[li[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(poster(movie_id))
    return recommend_movies, recommended_movies_poster


st.title("Movie Recommender System")
movie_name_opt = st.selectbox(
    'Select any movie you like and get five other related movies recommended',
    movies_list)
if st.button('Recommend'):
    names, poster = recommend(movie_name_opt)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])
