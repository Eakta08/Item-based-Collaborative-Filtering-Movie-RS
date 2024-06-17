import pickle
import streamlit as st
import requests
import re

def fetch_poster(movie_name):
    pattern=r'[\w\s:-]+'
    movie_name = re.search(pattern,movie_name).group().strip()
    print(movie_name)
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'query': movie_name,
        'api_key': '8265bd1679663a7ea12ac168da84d2e8', 
        'language': 'en-US'
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    movie = data['results'][0]
    poster_path = movie.get('poster_path')
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_recommendations(movie_title, similarity_matrix, data):
    sim_scores = similarity_matrix[movie_title]
    # Creating a threshold of selecting movies > 0.5 similarity
    sim_scores = sim_scores[sim_scores>=0.5].sort_values(ascending=False)
    # Get the top 5 similar movies
    top_similar_movies = sim_scores.drop(movie_title).head(5) 
    recommended_movie_names = [movie for movie in top_similar_movies.index]
    recommended_movie_posters = []
    for movie in recommended_movie_names:
        # fetch the movie poster
        #print(fetch_poster(movie))
        recommended_movie_posters.append(fetch_poster(movie))
    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
data = pickle.load(open('data.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = [movie for movie in data.columns]
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = get_recommendations(selected_movie,similarity,data)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
