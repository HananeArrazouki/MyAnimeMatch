import streamlit as st
import pandas as pd
import joblib
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os

# Especificar el directorio donde se encuentran los datos de NLTK
nltk_data_path = os.path.join(os.path.dirname(__file__), '..', 'nltk_data')
nltk.data.path.append(nltk_data_path)

# Inicializar el analizador de sentimientos
sid = SentimentIntensityAnalyzer()

# Cargar el modelo y el vectorizador
modelo_knn = joblib.load('models/modelo_knn_animo.pkl')
vectorizer = joblib.load('models/vectorizer_animo.pkl')

# Cargar el DataFrame con la columna 'Animo'
df = pd.read_csv('models/scraping_animeList_de_animo.csv')

# Función para obtener recomendaciones basadas en el estado de ánimo
def recomendar_animes(estado):
    animes = df[df['Animo'] == estado]
    if animes.empty:
        return pd.DataFrame()

    random_anime = animes.sample(1)
    anime_index = random_anime.index[0]

    X_tfidf_anime = vectorizer.transform([df['Synopsis'][anime_index]])
    distances, indices = modelo_knn.kneighbors(X_tfidf_anime)

    recomendados = df.iloc[indices[0]]
    return recomendados

# Función principal para la página de recomendaciones por estado de ánimo
def recommend_anime_sentiment():
    st.title("Recomendaciones de Animes por Estado de Ánimo")
    
    estado = st.selectbox("¿Cómo te sientes hoy?", ["feliz", "triste", "neutral"])
    
    if st.button("Obtener Recomendaciones"):
        recomendaciones = recomendar_animes(estado)
        if not recomendaciones.empty:  # Verificar si hay recomendaciones
            st.write(f"Animes recomendados para cuando estás {estado}:")
            for _, anime in recomendaciones.iterrows():
                col1, col2 = st.columns(2)
                with col1:
                    st.image(anime['Image_URL'], caption=anime['Title'], width=200)
                with col2:
                    st.write(f"**Título:** {anime['Title']}", style={"margin-left": "20px"})
                    # Verificar si Demographic está vacío o nulo
                    if pd.isna(anime['Demographic']) or anime['Demographic'] == '':
                        st.write("**Demographic:** Unknown")
                    else:
                        st.write(f"**Demographic:** {anime['Demographic']}")
                    st.write(f"**Popularity:** {anime['Popularity']}")
                    st.write(f"**Genres:** {anime['Genres']}")
                    st.write(f"**Score:** {anime['Score']}")
        else:
            st.write(f"No se encontraron animes para el estado de ánimo '{estado}'.")
