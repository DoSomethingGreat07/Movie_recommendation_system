import pickle
import streamlit as st
import requests

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        font-family: "Segoe UI", sans-serif;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        padding: 0.5em 1.5em;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title('🎬 Movie Recommender System')
st.subheader('Get movie suggestions with posters based on your favorite!')

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    names, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return names, posters

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Choose a movie", movie_list)

if st.button('🎯 Show Recommendations'):
    with st.spinner('Generating recommendations...'):
        names, posters = recommend(selected_movie)
        st.markdown("### 📌 Top Picks For You")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])

st.markdown("---")
st.markdown("Made by Nikhil using [Streamlit](https://streamlit.io) and TMDB API.")
