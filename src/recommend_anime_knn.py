import streamlit as st
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import joblib
import numpy as np

"""
    Une múltiples archivos en uno solo.
    
    :param output_path: Ruta del archivo combinado
    :param part_paths: Lista de rutas de las partes del archivo
"""
def combine_files(output_path, part_paths):
    with open(output_path, 'wb') as output_file:
        for part_path in part_paths:
            with open(part_path, 'rb') as part_file:
                output_file.write(part_file.read())

def combine_model_parts():
    part_files = [
        'models/modelo_knn2.pkl.part0', 
        'models/modelo_knn2.pkl.part1',
        'models/modelo_knn2.pkl.part2',
        'models/modelo_knn2.pkl.part3',
        'models/modelo_knn2.pkl.part4',
        'models/modelo_knn2.pkl.part5',
        'models/modelo_knn2.pkl.part6',
        'models/modelo_knn2.pkl.part7',
    ]
    combine_files('models/modelo_knn2.pkl', part_files)

# Unir las partes del modelo al iniciar la aplicación
combine_model_parts()

# Cargar el modelo KNN desde el archivo .pkl
modelo_knn = joblib.load("models/modelo_knn2.pkl")

# Cargar el vectorizador TF-IDF desde el archivo .pkl
vectorizer = joblib.load("models/vectorizer2.pkl")

# Cargar el DataFrame con los nombres de anime
df = pd.read_csv('models/scraping_animeList.csv')

def preprocess_text(text):
    # Dejamos solo palabras alfabéticas
    text = ' '.join(re.findall(r'\b[a-zA-Z]+\b', str(text)))
    # Eliminamos espacios adicionales
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

# Aplicar las mismas transformaciones que durante el entrenamiento
df.drop(['ID', 'Demographic', 'Licensors', 'Studios', 'Producers'], axis=1, inplace=True)
df.dropna(axis=0, inplace=True)

df.Episodes = df.Episodes.astype(int)
df.Score = df.Score.astype(int)
df.Ranked = df.Ranked.astype(int)
df.Members = df.Members.str.replace(',','').astype(int)
df.Favorites = df.Favorites.str.replace(',','').astype(int)

cols = ['Type', 'Source', 'Rating']
le = LabelEncoder()
for col in cols:
    df[col] = le.fit_transform(df[col])

df_genres = df.Genres.str.get_dummies(sep=',')
df_num = pd.concat([df.drop('Genres', axis=1), df_genres], axis=1)

df_num = df_num[~df_num['Synopsis'].str.contains('No synopsis information')]
df_num['Synopsis'] = df_num['Synopsis'].apply(preprocess_text)

# Obtener los nombres y las URLs de las imágenes de anime
nombres_anime = df_num['Title'].values
imagenes_anime = df['Image_URL'].values

# Definir el escalador y ajustarlo a los datos numéricos
scaler = MinMaxScaler()
scaler.fit(df_num.drop(['Title', 'Image_URL', 'Synopsis'], axis=1))

# Función para obtener recomendaciones
def obtener_recomendaciones(nombre_anime_usuario):
    try:
        # Obtener el índice del anime ingresado
        movie_index = np.where(nombres_anime == nombre_anime_usuario)[0][0]

        # Obtener el vector TF-IDF del título del anime ingresado
        synopsis_anime = df_num['Synopsis'].iloc[movie_index]
        nombre_anime_vectorizado = vectorizer.transform([synopsis_anime])

        # Obtener los datos numéricos del anime ingresado y escalarlos
        datos_numericos_anime = df_num.drop(['Title', 'Image_URL', 'Synopsis'], axis=1).iloc[movie_index]
        datos_numericos_anime_escalados = scaler.transform([datos_numericos_anime])

        # Combinar el vector TF-IDF y los datos numéricos escalados
        X_input = np.hstack((datos_numericos_anime_escalados, nombre_anime_vectorizado.toarray()))

        # Obtener vecinos más cercanos
        distances, indices = modelo_knn.kneighbors(X_input)

        # Obtener los nombres y las URLs de las imágenes de los animes más cercanos
        animes_cercanos = [{'Title': nombres_anime[i], 'Image_URL': imagenes_anime[i]} for i in indices.flatten()[1:]]  # Excluimos el anime de entrada

        return animes_cercanos
    except IndexError:
        return [{"Title": "Anime no encontrado. Por favor, introduce un título válido.", "Image_URL": None}]

def recommend_anime_knn():
    # Configuración de la interfaz de Streamlit
    st.title("Recomendador de Animes")
    nombre_anime_usuario = st.text_input("Introduce el título de un anime:")

    if st.button("Obtener Recomendaciones"):
        recomendaciones = obtener_recomendaciones(nombre_anime_usuario)
        st.write(f"Animes recomendados similares a {nombre_anime_usuario}:")
        for i, anime in enumerate(recomendaciones, 1):
            col1, col2 = st.columns(2)
            with col1:
                if anime['Image_URL']:
                    st.image(anime['Image_URL'], caption=anime['Title'], width=100)
                else:
                    st.write("Imagen no disponible")
            with col2:
                st.write(f"**Título:** {anime['Title']}")
            st.write("")
