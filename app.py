import pickle
import streamlit as st
import requests
import os

# --- Page Config ---
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="wide"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        body {
            background-color: #000;
        }
        .stApp {
            background: url('https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=1950&q=80');
            background-size: cover;
            background-position: center;
        }
        .glass-box {
            background: rgba(0, 0, 0, 0.7);
            padding: 2rem;
            border-radius: 16px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        .title {
            text-align: center;
            font-size: 3rem;
            color: white;
            margin-bottom: 1rem;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #f0f0f0;
            margin-bottom: 2rem;
        }
        .footer {
            text-align: center;
            color: #ccc;
            margin-top: 4rem;
            font-size: 0.9rem;
        }
        .social-icons a {
            margin: 0 10px;
            color: #f0f0f0;
            font-size: 1.5rem;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', "")
    return f"http://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    names, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        names.append(movies.iloc[i[0]]['title'])
        posters.append(fetch_poster(movie_id))
    return names, posters

# --- Load Data ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movie_path = os.path.join(BASE_DIR, 'artifacts', 'movie_list.pkl')
similarity_path = os.path.join(BASE_DIR, 'artifacts', 'similarity.pkl')

with open(movie_path, 'rb') as f:
    movies = pickle.load(f)

with open(similarity_path, 'rb') as t:
    similarity = pickle.load(t)

# --- Content ---
st.markdown('<div class="glass-box">', unsafe_allow_html=True)

st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Built with Machine Learning </div>', unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Type a movie to get recommendations:", movie_list)

if st.button('🎥 Show Recommendations'):
    with st.spinner("Fetching recommendations..."):
        recommended_names, recommended_posters = recommend(selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(recommended_posters[i])
                st.caption(recommended_names[i])

st.markdown("</div>", unsafe_allow_html=True)  # close glass box

# --- Footer with Links ---
st.markdown("""
<div class="footer">
    Connect with me:
    <div class="social-icons">
        <a href="https://github.com/subhvm" target="_blank">🐙</a>
        <a href="https://www.linkedin.com/in/subham-chaudhary-81961ba0/" target="_blank">💼</a>
        <a href="mailto:subhamchaudhary9818@gmail.com">✉️</a>
    </div>
    <br>Subham Chaudhary
</div>
""", unsafe_allow_html=True)
